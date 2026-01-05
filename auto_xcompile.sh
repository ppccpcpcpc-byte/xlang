#!/bin/sh

# 사용법 체크
if [ $# -ne 1 ]; then
    echo "Usage: $0 <file.x>"
    exit 1
fi

SRC="$1"

# 확장자 체크
case "$SRC" in
    *.x) ;;
    *)
        echo "Error: .x file only"
        exit 1
        ;;
esac

BASE="${SRC%.x}"
XBIN="$BASE.xbin"
XRUN="$BASE.xrun"

echo "[*] compiling $SRC → $XBIN"
python -c "from xcompiler import compile_x, save_xbin; save_xbin(compile_x('$SRC'), '$XBIN')" || exit 1

echo "[*] packing $XBIN → $XRUN"
python -c "from xcompiler import pack_xrun; pack_xrun('$XBIN', '$XRUN')" || exit 1

chmod +x "$XRUN"

echo "[DONE] $XRUN created"
