def fullSHA
def shortSHA
def branch
def commitMessage

def sendSlackMessage(statusMessage, commitMessage, shortSHA, fullSHA) {
    echo "Your pipeline has been ${statusMessage}"
    echo "Commit Message: ${commitMessage}"
    echo "Tags: ${shortSHA}, ${fullSHA}"
}

pipeline {
    agent any
    environment {
        DOCKER_REPOSITORY = 'sysnet4admin/worklog-backend'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        ARGOCD_SERVER = 'argocd-server.argocd.svc.cluster.local'
        ARGOCD_APP_NAME = 'worklog-backend'
        ARGOCD_ADMIN_PASSWORD = credentials('argocd-admin-password')
        GITHUB_CREDENTIALS = credentials('github-token')
    }
    stages {
        stage('Init Variables') {
            steps {
                script {
                    fullSHA = sh(script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
                    shortSHA = fullSHA[0..8]
                    branch = env.BRANCH_NAME
                    commitMessage = sh(script: "git log -1 --format='*%s* by _%an_'", returnStdout: true)
                }
            }
        }
        stage('Run Test') {
            steps {
                script {
                    echo "let's run a test for ${shortSHA} in ${branch}"
                    echo "running test for ${fullSHA}"
                    sh '''
                        curl -LsSf https://astral.sh/uv/install.sh | sh
                        export PATH="$HOME/.local/bin:$PATH"
                        uv sync --extra dev
                        TESTING=true uv run coverage run --source ./src/worklog -m pytest --disable-warnings -v
                        uv run coverage report
                    '''
                }
            }
        }
        stage('Build and Push Image') {
            steps {
                script {
                    echo "Let's build the image for ${shortSHA} in ${branch}"

                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        sh """
                            docker run --privileged --rm tonistiigi/binfmt --install all 2>/dev/null || true
                            docker buildx create --use --name multi-platform-builder 2>/dev/null || true
                            docker buildx build \
                                --platform linux/amd64,linux/arm64 \
                                -t ${DOCKER_REPOSITORY}:${shortSHA} \
                                -t ${DOCKER_REPOSITORY}:${fullSHA} \
                                --push .
                        """
                    }

                    echo 'build successful and published image with the following tags:'
                    echo "Tags: ${shortSHA}, ${fullSHA}"
                }
            }
        }
        stage('Update Manifest') {
            steps {
                sh """
                    sed -i "s|image: .*worklog-backend:.*|image: ${DOCKER_REPOSITORY}:${shortSHA}|" deploy_manifest/worklog-backend.yaml
                    sed -i "s|value: .* # IMAGE_TAG|value: ${shortSHA} # IMAGE_TAG|" deploy_manifest/worklog-backend.yaml
                    git config user.name "jenkins"
                    git config user.email "jenkins@myk8s.local"
                    git remote set-url origin https://${GITHUB_CREDENTIALS_USR}:${GITHUB_CREDENTIALS_PSW}@github.com/sysnet4admin/worklog-backend.git
                    git add deploy_manifest/
                    git commit -m "deploy: update image tag to ${shortSHA}"
                    git push origin main
                """
            }
        }
        stage('Sync Argo CD') {
            steps {
                sh """
                    argocd login ${ARGOCD_SERVER} \
                        --username admin \
                        --password ${ARGOCD_ADMIN_PASSWORD} \
                        --insecure
                    argocd app sync ${ARGOCD_APP_NAME}
                    argocd app wait ${ARGOCD_APP_NAME} --health --timeout 120
                """
                echo "Argo CD sync completed successfully"
            }
        }
    }
    post {
        always {
            echo 'Job finished. Sending slack notifications ..'
        }
        success {
            echo 'Build Success, Notifying to slack..'
            sendSlackMessage('completed', commitMessage, shortSHA, fullSHA)
        }
        failure {
            echo 'Build Failed, Notifying to slack..'
            sendSlackMessage('failed', commitMessage, shortSHA, fullSHA)
        }
        aborted {
            echo 'Build Aborted, Notifying to slack..'
            sendSlackMessage('aborted', commitMessage, shortSHA, fullSHA)
        }
    }
}
