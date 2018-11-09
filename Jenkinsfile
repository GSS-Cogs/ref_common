pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'cloudfluff/csvlint'
                    reuseNode true
                }
            }
            steps {
                script {
                    List<String[]> codelists = readFile('codelists.csv').split('\n').tail().collect {
                        l -> l.split(',')
                    }
                    for (String[] row : codelists) {
                        codelistFilename = "codelists/${row[1]}"
                        sh "csvlint -s codelist-schema.json ${codelistFilename}"
                    }
                }
            }
        }
    }
}
