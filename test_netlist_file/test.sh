#! /bin/bash

args=$(getopt i $*) || exit 1
# args=`getopt abc $*` 同等の意味の古い書き方

set -- $args
# eval "set -- $args" # zsh の shwordsplit に対応するにはこちらを使う

I_FLAG=0
# オプション解析のためのループ
for opt in "$@"; do # in "$@" を省略して for opt と書くことも出来ます。
    case $opt in
        -i) I_FLAG=1; shift ;;
        --) shift; break ;;
        *) echo "Unknown option: -$OPTARG" >&2; exit 1 ;;
    esac
done

# 引数の数の確認
if [ $# -eq 1 ]; then
    filepath=$1
else
    echo "Invalid argument" >&2
    exit 1
fi

# ファイルのパスの確認
if [ -f $filepath ]; then
    echo "Exist"
    abspath=$(cd $(dirname $1) && pwd)/$(basename $1)
    echo "Absolute Path: ${abspath}"
    # python /opt/sim-plot.py ${abspath}
else
    echo "file does not exist: ${abspath}" >&2
    exit 1
fi

str="\*+\s*test\s*\*+"
if [ $I_FLAG -eq 1 ]; then
    # 初期化処理
    if grep -E ${str} $abspath; then 
        echo "Already initialized" >&2
    else
        sed -i -e '$a \\n\n*** test ***\nAvalue=\nBvalue=\nCvalue=' ${abspath}
        echo "Initialization completed"
    fi
else
    # 実行処理(確認したい)
    echo "opti"
    # 実行処理(確認したい)
    if grep -E ${str} $abspath; then 
        echo "opti"
    else
        sed -i -e '$a \\n\n*** test ***\nAvalue=\nBvalue=\nCvalue=' ${abspath}
        echo "Optimization variables are not described" >&2
        echo 'Please run "opt -i <filepath>" to initialize it'
    fi
fi
