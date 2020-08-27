@Library('pmd@family-pmd4') _

import uk.org.floop.jenkins_pmd.Drafter

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
                    alwaysPull true
                }
            }
            steps {
                script {
                    ansiColor('xterm') {
                        sh "csvlint -s measures.csv-metadata.json"
                    }
                }
            }
        }
        stage('Convert to RDF') {
            agent {
                docker {
                    image 'gsscogs/csv2rdf'
                    reuseNode true
                    alwaysPull true
                }
            }
            steps {
                script {
                    sh "mkdir -p out/ontologies out/concept-schemes"
                    sh "csv2rdf -t 'measures.csv' -u 'measures.csv-metadata.json' -m annotated -o out/ontologies/measures.ttl"
                    for (def metadata : findFiles(glob: "codelists/*.csv-metadata.json")) {
                        String baseName = metadata.name.substring(0, metadata.name.lastIndexOf('.csv-metadata.json'))
                        sh "csv2rdf -t 'codelists/${baseName}.csv' -u 'codelists/${metadata.name}' -m annotated > 'out/concept-schemes/${baseName}.ttl'"
                    }
                }
            }
        }
        stage('Upload') {
            agent {
                docker {
                    image 'gsscogs/csv2rdf'
                    reuseNode true
                    alwaysPull true
                }
            }
            steps {
                script {
                    def pmd = pmdConfig('pmd')
                    for (myDraft in pmd.drafter
                            .listDraftsets(Drafter.Include.OWNED)
                            .findAll { it['display-name'] == env.JOB_NAME }) {
                        pmd.drafter.deleteDraftset(myDraft.id)
                    }
                    def id = pmd.drafter.createDraftset(env.JOB_NAME).id
                    for (graph in util.jobGraphs(pmd, id)) {
                        pmd.drafter.deleteGraph(id, graph)
                        echo "Removing own graph ${graph}"
                    }
                    def uploads = []
                    writeFile file: "ontgraph.sparql", text:  """SELECT ?graph { ?graph a <http://www.w3.org/2002/07/owl#Ontology> }"""
                    for (def ontology : findFiles(glob: 'out/ontologies/*')) {
                        sh "sparql --data='${ontology.path}' --query=ontgraph.sparql --results=JSON > 'graph.json'"
                        uploads.add([
                            "path": ontology.path,
                            "format": "text/turtle",
                            "graph": readJSON(text: readFile(file: "graph.json")).results.bindings[0].graph.value
                        ])
                    }
                    writeFile file: "csgraph.sparql", text:  """SELECT ?graph { ?graph a <http://www.w3.org/2004/02/skos/core#ConceptScheme> }"""
                    for (def cs : findFiles(glob: 'out/concept-schemes/*')) {
                        sh "sparql --data='${ontology.path}' --query=csgraph.sparql --results=JSON > 'graph.json'"
                        uploads.add([
                                "path": cs.path,
                                "format": "text/turtle",
                                "graph": readJSON(text: readFile(file: "graph.json")).results.bindings[0].graph.value
                        ])
                    }
                    for (def upload: uploads) {
                        pmd.drafter.addData(id, "${WORKSPACE}/${upload.path}", upload.format, "UTF-8", upload.graph)
                        writeFile(file: "${upload.path}-prov.ttl", text: util.jobPROV(upload.graph))
                        pmd.drafter.addData(id, "${WORKSPACE}/${upload.path}-prov.ttl", "text/turtle", "UTF-8", upload.graph)
                    }
                    pmd.drafter.publishDraftset(id)
                }
            }
        }
        post {
            always {
                script {
                    archiveArtifacts artifacts: "out/"
                }
            }
        }
    }
}