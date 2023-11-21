# cow_skin_check

nohup tensorflow_model_server \
  --rest_api_port=8502 \
  --model_name=fashion_model \
  --model_base_path="${MODEL_DIR}" >server.log 2>&1
