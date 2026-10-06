#!/bin/bash
#SBATCH --job-name=chandra-p66
#SBATCH --gres=gpu:3g.40gb:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:45:00
#SBATCH --output=%x-%j.out
# Re-OCR one page (Tropical Agriculturist vol. 3, p. 66, scan n83) with Chandra 2, three times,
# to see whether the two wrong sentences in output_v6 reproduce. Serving block from
# /project/clifford/tropical/run_volume_plato.slurm.
set -uo pipefail
W=/project/clifford/trimen_workshop/chandra_p66
SIF=$HOME/projects/def-jic823/containers/vllm-openai-v0.17.0.sif
MODEL_CACHE=$HOME/projects/def-jic823/models
MODEL=datalab-to/chandra-ocr-2
VENV=$HOME/chandra_plato/venv
module load apptainer cuda/12.6
mkdir -p "$W/out" "$HOME/.apptainer/tmp"; export APPTAINER_TMPDIR="$HOME/.apptainer/tmp"
PORT=$(python3 -c 'import socket;s=socket.socket();s.bind(("127.0.0.1",0));print(s.getsockname()[1]);s.close()')
echo "node $(hostname) job $SLURM_JOB_ID port $PORT $(date -Is)"
apptainer exec --nv --bind "$MODEL_CACHE:/root/.cache/huggingface" --bind "$HOME:$HOME" --bind /project/clifford:/project/clifford \
    --bind /etc/pki:/etc/pki --bind /etc/ssl:/etc/ssl \
    --env HF_HOME=/root/.cache/huggingface --env HF_HUB_OFFLINE=1 --env HF_HUB_DISABLE_XET=1 \
    --env REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt --env SSL_CERT_FILE=/etc/pki/tls/certs/ca-bundle.crt \
    "$SIF" vllm serve "$MODEL" --host 127.0.0.1 --port "$PORT" --served-model-name chandra --dtype bfloat16 \
    --max-model-len 18000 --max-num-seqs 4 --max_num_batched_tokens 8192 --gpu-memory-utilization 0.90 \
    --enable-prefix-caching --no-enforce-eager --mm-processor-kwargs '{"min_pixels": 3136, "max_pixels": 6291456}' \
    > "$W/vllm-$SLURM_JOB_ID.log" 2>&1 &
VLLM_PID=$!
trap 'kill $VLLM_PID 2>/dev/null || true' EXIT INT TERM
for i in $(seq 1 120); do
    code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:${PORT}/v1/models" 2>/dev/null || echo 000)
    [ "$code" = "200" ] && { echo "server ready after $((i*10))s"; break; }
    kill -0 "$VLLM_PID" 2>/dev/null || { echo "SERVER DIED"; tail -40 "$W/vllm-$SLURM_JOB_ID.log"; exit 1; }
    sleep 10
done
source "$VENV/bin/activate"
export VLLM_API_BASE="http://127.0.0.1:${PORT}/v1" VLLM_MODEL_NAME=chandra VLLM_API_KEY=EMPTY
for k in 1 2 3; do
    echo "--- run $k $(date -Is)"
    chandra "$W/n83.jpg" "$W/out/run$k" --method vllm --max-workers 1 --batch-size 1 --no-images
    find "$W/out/run$k" -name '*.md' -exec sh -c 'echo "== $1"; grep -n -i "years old from the time\|possession the bark\|prints of the leaves\|bad situation\|full condition\|many plants" "$1"' _ {} \;
done
echo "done $(date -Is)"
