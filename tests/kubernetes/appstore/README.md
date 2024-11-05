# appstore namespace

Covered in tests:
* [x] deployment.apps/appstore-h2oaicloud-server  with availability being the replica count (1 for default)
* [x] configmap/appstore-h2oaicloud-conf should exist
* [x] service/appstore-service reading port 80
* [ ] pvc/appstore-h2oaicloud-pvc should exist abd be Bound to the appstore pod if using pvc for storage
* [x] pod/appstore-server-{} Number of pods equals to the replica count
    * [x] Should have the configmap/appstore-h2oaicloud-conf mounted to /config
    * [ ]  Should have the volume  pvc/appstore-h2oaicloud-pvc mounted to /var/lib/wave/store (only for pvc)
* [x] secret appstore-h2oaicloud-secrets should exist with keys
    * [x] dsn key
    * [x] clientSecret and waveClientSecret
    * [x] sessionKey
* [ ] secret appstore-postgresql should exist if postgres is deployed
* [ ] statefulset.apps/appstore-postgresql should exist if postgres is deployed
* [ ] /d/alive endpoint should return OK
* [x] Ingress pointing to wildcard subdomain "*.appstore.h2o.ai"  and main domain "appstore.h2o.ai"
* [ ] Ingress should have a route /.ai.h2o.cloud.discovery/ that points to the h2oaicloud-discovery-service 
* [x] Service Account appstore-h2oaicloud-service-account should exist

# appstore-apps namespace

* [ ] appstore-h2oaicloud-app-service-account should exist