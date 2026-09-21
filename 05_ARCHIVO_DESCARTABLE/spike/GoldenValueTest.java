import ai.onnxruntime.OrtException;
import ai.onnxruntime.OrtSession;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

import SQ.TALibIndicators.QlibSignal.OnnxModelManager;
import SQ.TALibIndicators.QlibSignal.QlibSignalCore;

/**
 * Arnes standalone del gate de valores dorados (Tarea T4 de
 * Qlib_ONNX_Bridge_Design.md). Lee EXACTAMENTE la misma ventana de precios
 * que export_golden_values.py exporto a close_prices.csv, corre
 * QlibSignalCore.computeSignal() (la MISMA logica que usara QlibSignal.java
 * real dentro de SQX), y escribe java_predictions.csv para que
 * compare_golden_values.py (Python) haga la comparacion final bar-a-bar.
 *
 * NO corre dentro de SQX -- corre el JDK embebido real de SQX
 * (j64\bin\java.exe) apuntando a los artefactos de prueba via las system
 * properties qlibsignal.model.path / qlibsignal.spec.path (ver
 * OnnxModelManager.java), NO a C:\SQX_144_Full (protegido, y este es un
 * modelo de prueba sintetico, no el real).
 */
public class GoldenValueTest {
    public static void main(String[] args) throws Exception {
        String closeCsvPath = args.length > 0 ? args[0] : "qlib_export/output/close_prices.csv";
        String outCsvPath = args.length > 1 ? args[1] : "qlib_export/output/java_predictions.csv";

        System.out.println("=== 1. Leer close_prices.csv (misma ventana que uso Python) ===");
        float[] closePrices = readCloseColumn(closeCsvPath);
        System.out.println("OK: " + closePrices.length + " precios leidos de " + closeCsvPath);

        System.out.println("\n=== 2. Cargar sesion ONNX (OnnxModelManager, misma clase que usa QlibSignal real) ===");
        long tSession0 = System.nanoTime();
        OrtSession session = OnnxModelManager.getSession();
        long tSession1 = System.nanoTime();
        if (session == null) {
            System.out.println("RESULT: FAIL - OnnxModelManager.getSession() devolvio null: " +
                OnnxModelManager.getLoadFailureReason());
            System.exit(1);
        }
        OnnxModelManager.FeatureSpec spec = OnnxModelManager.getFeatureSpec();
        System.out.println("OK: getSession() tardo " + ((tSession1 - tSession0) / 1_000_000) + " ms");
        System.out.println("OK: sesion cargada, spec_hash=" + spec.specHash +
            ", lookback=" + spec.lookbackBars + ", features=" + String.join(",", spec.featureNames));

        System.out.println("\n=== 3. Computar senal via QlibSignalCore.computeSignal() (misma logica que QlibSignal.java) ===");
        long tCompute0 = System.nanoTime();
        float[] predictions;
        try {
            predictions = QlibSignalCore.computeSignal(
                closePrices, OnnxModelManager.getEnvironment(), session, spec
            );
            long tCompute1 = System.nanoTime();
            System.out.println("OK: computeSignal() tardo " + ((tCompute1 - tCompute0) / 1_000_000) + " ms");
        } catch (OrtException e) {
            System.out.println("RESULT: FAIL - OrtException: " + e.getMessage());
            System.exit(1);
            return;
        }
        System.out.println("OK: " + predictions.length + " predicciones computadas " +
            "(las primeras " + spec.lookbackBars + " son NaN, warm-up esperado)");

        System.out.println("\n=== 4. Escribir java_predictions.csv ===");
        try (PrintWriter w = new PrintWriter(new FileWriter(outCsvPath))) {
            w.println("local_index,java_prediction");
            for (int i = 0; i < predictions.length; i++) {
                w.println(i + "," + predictions[i]);
            }
        }
        System.out.println("OK: " + outCsvPath + " escrito");

        System.out.println("\n=== COMPLETADO ===");
    }

    private static float[] readCloseColumn(String csvPath) throws Exception {
        List<Float> values = new ArrayList<>();
        try (BufferedReader r = new BufferedReader(new FileReader(csvPath))) {
            String header = r.readLine(); // "timestamp,close"
            int closeIdx = header.split(",").length - 1; // ultima columna
            String line;
            while ((line = r.readLine()) != null) {
                String[] parts = line.split(",");
                values.add(Float.parseFloat(parts[closeIdx]));
            }
        }
        float[] out = new float[values.size()];
        for (int i = 0; i < out.length; i++) out[i] = values.get(i);
        return out;
    }
}
