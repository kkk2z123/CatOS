; boot.asm

BITS 16                 ; 16ビットモードで動作

start:
    cli                 ; 割り込みを無効化
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00      ; スタックポインタを設定
    sti                 ; 割り込みを有効化

    ; カーネルをロード
    mov bx, 0x1000      ; カーネルのロード先アドレス
    mov dh, 0           ; ヘッド
    mov dl, 0           ; ドライブ
    mov cx, 2           ; セクタ数
    mov ax, 0x0201      ; 読み込みコマンド
    int 0x13            ; BIOS割り込みでディスク読み込み

    ; Cカーネルにジャンプ
    jmp 0x1000:0000

; ディスクのシグネチャ
times 510-($-$$) db 0
dw 0xAA55
