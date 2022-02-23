INPUT_DIR=./datasets/lichess
OUTPUT_DIR=./datasets/lichess-sampled

mkdir -p $OUTPUT_DIR
input_files=$(find $INPUT_DIR -type f -name "*.pgn.bz2")

function to_human_readable {
    numfmt --to=iec-i --suffix=B --padding=7 $1
}

# count the total size of the input files
total_size=0
for file in $input_files; do
    total_size=$(($total_size + $(stat -c %s $file)))
done

echo $(to_human_readable $total_size) total

processed_size=0

for f in $input_files; do
    input_file=$(basename $f .pgn.bz2)
    year=$(basename $(dirname $f))
    output_file="$OUTPUT_DIR/$year/$input_file.sampled.pgn.bz2"
    mkdir -p $(dirname $output_file)
    echo "$f -> $output_file"
    pv $f | pbzip2 -dck | python splitting.py | pbzip2 -z > $output_file
    size=$(stat -c%s $f)
    processed_size=$(($processed_size + $size))
    echo Processed $(to_human_readable $processed_size) of $(to_human_readable $total_size)
done