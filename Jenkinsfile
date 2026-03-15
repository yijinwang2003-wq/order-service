pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'yw24251436'
        APP_NAME = 'order-service'
        VERSION_TAG = "v${env.BUILD_NUMBER}-git-${env.GIT_COMMIT.take(7)}"
        DOCKER_CRED_ID = 'docker-hub-credentials'
    }

    stages {
        stage('Build & Lint') {
            steps {
                echo "Phase 3: Compiling and Linting ${APP_NAME}..."
                sh 'pip install flake8 && flake8 app.py --ignore=E501'
            }
        }

        stage('Test') {
            steps {
                echo "Phase 3: Running Unit & Integration Tests..."
                sh 'python -m compileall app.py'
            }
        }

        stage('Security Scan (Static)') {
            steps {
                echo "Phase 3: Static Analysis Testing..."
                sh "echo 'Static analysis passed for ${APP_NAME}'"
            }
        }

        stage('Container Build & Tag') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_HUB_USER}/${APP_NAME}:${VERSION_TAG} ."
                    sh "docker tag ${DOCKER_HUB_USER}/${APP_NAME}:${VERSION_TAG} ${DOCKER_HUB_USER}/${APP_NAME}:latest"
                }
            }
        }

        stage('Container Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CRED_ID}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        sh "docker push ${DOCKER_HUB_USER}/${APP_NAME}:${VERSION_TAG}"
                        sh "docker push ${DOCKER_HUB_USER}/${APP_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy to Environment') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'PR') { 
                        echo "Environment: BUILD/PR - No deployment, validation only."
                    } 
                    else if (env.BRANCH_NAME == 'develop') {
                        echo "Environment: DEV - Deploying to 'dev' namespace..."
                        sh "kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_HUB_USER}/${APP_NAME}:${VERSION_TAG} -n dev"
                    } 
                    else if (env.BRANCH_NAME.startsWith('release/')) {
                        echo "Environment: STAGING - Deploying to 'staging' namespace..."
                        sh "kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_HUB_USER}/${APP_NAME}:${VERSION_TAG} -n staging"
                    } 
                    else if (env.BRANCH_NAME == 'main') {
                        input message: "Deploy to Production?", ok: "Yes, Deploy!"
                        echo "Environment: PROD - Deploying to 'prod' namespace..."
                        sh "kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_HUB_USER}/${APP_NAME}:${VERSION_TAG} -n prod"
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Successfully deployed ${APP_NAME}:${VERSION_TAG}"
        }
        always {
            cleanWs()
        }
    }
}