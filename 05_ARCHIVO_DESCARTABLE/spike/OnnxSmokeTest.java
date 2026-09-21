import ai.onnxruntime.OrtEnvironment;

/**
 * Spike P1 (TODOS.md) / Tarea T0a (Qlib_ONNX_Bridge_Design.md).
 * Pregunta única: ¿carga onnxruntime-java (via JNI) bajo el JDK embebido real
 * de SQX (OpenJDK 25.0.1 LTS Zulu, Windows) sin errores de acceso nativo (JEP 472)?
 *
 * Deliberadamente NO usa el classloader custom de snippets de SQX ni el modelo
 * ONNX real todavía -- eso es una pregunta distinta (hallazgo #5 de la revisión
 * "outside voice" de /plan-eng-review, sin resolver, fuera de alcance de este spike).
 * Este test solo prueba: JVM version + JNI native loading, aislado.
 */
public class OnnxSmokeTest {
    public static void main(String[] args) {
        System.out.println("java.version = " + System.getProperty("java.version"));
        System.out.println("java.vendor  = " + System.getProperty("java.vendor"));
        System.out.println("os.arch      = " + System.getProperty("os.arch"));

        try {
            long t0 = System.nanoTime();
            OrtEnvironment env = OrtEnvironment.getEnvironment();
            long t1 = System.nanoTime();
            System.out.println("RESULT: OK - OrtEnvironment cargado sin excepcion");
            System.out.println("  tiempo de carga JNI: " + ((t1 - t0) / 1_000_000) + " ms");
            System.out.println("  env = " + env);
        } catch (UnsatisfiedLinkError e) {
            System.out.println("RESULT: FAIL - UnsatisfiedLinkError (nativo no cargo)");
            e.printStackTrace();
            System.exit(1);
        } catch (Throwable e) {
            System.out.println("RESULT: FAIL - " + e.getClass().getSimpleName());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
