def AGENT_LABEL = null

node('master') {
  stage('Checkout and set agent'){
     checkout scm
     if (env.SLAVE) {
        AGENT_LABEL = env.SLAVE

     } else {
        AGENT_LABEL = "test-ravtech"
     }
     sh "echo ${AGENT_LABEL}"
   }
}

pipeline {
    agent { label "${AGENT_LABEL}" }
    stages {
        stage('Build zap env') {
             steps {
                 script{
//                     sh "docker image prune -a -f"
//                     sh "docker pull owasp/zap2docker-stable"
//                     sh "sudo chmod +x zap-docker.sh"
                    sh "docker-compose -f ./docker/docker-compose-selenium-zap.yml up -d zap"
//                     sh "export ZAP_IP=\$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' zap)"

                 }
             }
        }
         stage('build python tests and selenium'){
            environment{
                ZAP_IP="""${sh(
                            returnStdout: true,
                            script: 'docker inspect --format=\'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}\' zap'
                            )}"""
            }
            steps{
                script{
                    sh "echo $ZAP_IP"
                    sh "docker kill zap selenium-server python-tests || true"
                    sh "docker-compose -f ./docker/docker-compose-selenium-remote.yml build python-tests"
                    sh "docker-compose -f ./docker/docker-compose-selenium-remote.yml up -d selenium-server python-tests"
                    sh "docker wait python-tests"
                    sh "docker logs --details python-tests"
                    sh "echo /"python logs:/""
                    sh "docker logs --details zap"
                    sh "echo /"zap:/""
                    sh "docker-compose -f ./docker/docker-compose-selenium-remote.yml down"

                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: './zap_reports',
                        reportFiles: 'test.html',
                        reportName: 'ZAP  Report',
                        reportTitles: ''
                    ])
                }
            }
         }
    }
}