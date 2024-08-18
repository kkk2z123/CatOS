// kernel.c

void main() {
    // ここでBIOSによってリアルモードで動作しているので、モードの切り替えが必要です。

    // このコードは32ビット保護モードに切り替えられる前提で書かれています。
    // ブートローダで保護モードに移行させてから、Pythonインタープリタを呼び出します。

    // Pythonスクリプトの実行
    const char *python_command = "python shell.py";
    system(python_command);

    // 終了
    while (1);
}
