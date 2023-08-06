# Re-generate gRPC files

To re-generate the gRPC files, run: 
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./client_manager.proto
```
