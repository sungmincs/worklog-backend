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
            agent {
                docker {
                    image 'ghcr.io/astral-sh/uv:python3.12-bookworm-slim'
                }
            }
            steps {
                script {
                    echo "let's run a test for ${shortSHA} in ${branch}"
                    echo "running test for ${fullSHA}"
                    sh 'uv sync'
                    sh 'TESTING=true uv run coverage run --source ./src/worklog -m pytest --disable-warnings -v'
                    sh 'uv run coverage report'
                }
            }
        }
        stage('Build Image') {
            steps {
                echo "Let's build the image for ${shortSHA} in ${branch}"
                echo "The change commit message to build is '${commitMessage}'"
                echo 'build successful and published image with the following tags:'
                echo "Tags: ${shortSHA}, ${fullSHA}"
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
