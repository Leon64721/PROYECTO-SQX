package com.strategyquant.tradinglib;

/*
 * STUB LOCAL, SOLO PARA COMPILACION/PRUEBA STANDALONE FUERA DEL CODE EDITOR
 * REAL DE SQX. NO DESPLEGAR ESTE ARCHIVO A C:\SQX_144_Full -- ahi Log ya
 * existe de verdad (SQX lo inyecta internamente al compilar dentro de su
 * propio Code Editor).
 *
 * Confirmado empiricamente (Tarea T5): com.strategyquant.tradinglib.Log NO
 * existe como .class en ningun jar de internal\libs\ (ni siquiera contra el
 * classpath completo internal\libs\*) -- mismo patron ya documentado en
 * ClaudeCode_SQX_Notes.md para SettingsMap/IXMLAble/ISQCloneable. API real
 * confirmada por USO REAL (grep sobre 55 archivos fuente de fabrica en
 * internal\extend\Snippets), estilo SLF4J (coincide con logback-classic.jar/
 * slf4j-api.jar ya presentes en internal\libs\):
 *   Log.error("mensaje", excepcion)
 *   Log.debug("mensaje con {} placeholders", arg1, arg2, ...)
 *   Log.info("mensaje con {} placeholders", arg)
 */
public final class Log {
    private Log() { }

    public static void error(String msg, Throwable t) {
        System.err.println("[STUB Log.error] " + msg);
        if (t != null) t.printStackTrace();
    }

    public static void error(String msg) {
        System.err.println("[STUB Log.error] " + msg);
    }

    public static void debug(String msg, Object... args) {
        System.out.println("[STUB Log.debug] " + format(msg, args));
    }

    public static void info(String msg, Object... args) {
        System.out.println("[STUB Log.info] " + format(msg, args));
    }

    public static void warn(String msg, Object... args) {
        System.out.println("[STUB Log.warn] " + format(msg, args));
    }

    private static String format(String msg, Object... args) {
        String out = msg;
        for (Object a : args) {
            out = out.replaceFirst("\\{\\}", java.util.regex.Matcher.quoteReplacement(String.valueOf(a)));
        }
        return out;
    }
}
