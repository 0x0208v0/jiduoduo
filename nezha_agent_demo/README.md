# 参考：

https://git.kuzu.uk/pagent.git

# 生成代码

```shell

cd nezha_agent_demo

python -m grpc_tools.protoc -I./proto --python_out=./proto --pyi_out=./proto --grpc_python_out=./proto ./proto/nezha.proto

```