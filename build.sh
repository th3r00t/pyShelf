#!/usr/bin/env sh
# uv export > requirements.txt
# mkdir if not exists release
mkdir -p release
python -m zipapp src --compress --output=release/pyshelf --python="/usr/bin/env python"
exit 0
