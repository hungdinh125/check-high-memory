pipeline {
    agent any
    stages {
        stage('Clone the repository to container') {
            steps {
                sh 'git clone https://github.com/hungdinh125/check-high-memory.git'                
            }
        }
        stage('Enable virtual environment pyats') {
            steps {
                sh 'python3 -m venv pyats'
                sh 'source pyats/bin/activate'
            }
        }
        stage('Run the Python script apac_high_memory.py') {
            steps {
                sh 'python3 apac_high_memory.py --testbed apac_tb.yaml"'
            }
        }
        stage('Copy output to Jenkins server directory') {
            steps {
                sh 'scp apac_switch_memory.txt apacftp:P%40ssw0rd@10.133.10.115/apac_switch_memory.txt"'
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
