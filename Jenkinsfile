pipeline {
    agent any
    stages {
        stage('Enable virtual environment pyats') {
            steps {
                echo 'Setup PYATS environment'
                sh 'python3 -m venv pyats'
                sh 'source pyats/bin/activate'
            }
        }
        stage('List Files in Directory') {
            steps {
                echo 'Confirm required files are cloned'
                sh 'ls -la'
            }
        }        
        stage('Run the Python script apac_high_memory.py') {
            steps {
                echo 'Activate Python script to show used memory'
                sh 'python3 apac_high_memory.py --testbed apac_tb.yaml'
            }
        }
        stage('Output the result in console logging') {
            steps {
                echo 'Display Used Memory to console'
                sh 'cat apac_switch_memory.txt'
            }
        }
        stage('Post to MS Teams') {
            steps {
                echo 'Send result to MS Teams channel'
                script {
                    // Read and format the result
                    def result = sh(script: '''
                    sed ':a;N;$!ba;s/\\n/\\\\n/g' apac_switch_memory.txt | sed 's/\\"/\\\\\\"/g'
                    ''', returnStdout: true).trim()

                    // Escape double quotes in the result
                    def escapedResult = result.replace('"', '\\"')

                    // Format payload using Markdown
                    def payload = """{
                      "text": "```Memory status report:\\n\\n${escapedResult}```"
                    }"""

                    // Send payload to Microsoft Teams
                    sh(script: """
                    curl -H 'Content-Type: application/json' -d '${payload}' https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c
                    """)
                }
            }
        }
    }
    post {
        always {
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
        }
    }
}
