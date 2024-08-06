pipeline {
    agent any
    stages {
        stage('Clone the repository') {
            steps {
                sh 'git clone https://github.com/hungdinh125/check-high-memory.git'
            }
        }
        stage('Verify directory is clonded') {
            steps {
                sh 'ls -la'
            }
        }
        stage('Run the python script apac_high_memory.py') {
            steps {
                sh 'python3 apac_high_memory.py --testbed apac_tb.yaml'
            }
        }
        stage('Copy output to Jenkins server directory') {
            steps {
                sh 'cp check-high-memory/apac_switch_memory txt .'
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