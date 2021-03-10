CONSUL_HOST="172.17.0.1"

docker rm -f badger 2>/dev/null
docker run  -d  -p 8500:8500 --name=badger consul agent -server -ui -node=consul -bootstrap-expect=1 -client=0.0.0.0

function check_leader(){
    curl -XGET -I http://$CONSUL_HOST:8500/v1/health/node/consul | grep 'X-Consul-Knownleader: true'
}

while ! (check_leader) >/dev/null 2>&1
do
    echo "waiting for consul"
    sleep 1
done
echo "consul ready"
curl -XPUT  http://$CONSUL_HOST:8500/v1/kv/warehouses -d '[{"warehouse_id" :"warehouse_1","is_enabled":"true", "address": "warehouse_address_1"}, {"warehouse_id": "warehouse_2", "is_enabled": false, "address": "warehouse_address_2"}]' 


echo ""
echo "to test run: 'curl  http://$CONSUL_HOST:8500/v1/kv/warehouses?raw=true'"
