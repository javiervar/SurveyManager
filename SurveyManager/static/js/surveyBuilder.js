var app = angular.module('app', ['chart.js']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});


app.controller('surveysController', ['$scope', '$http', function($s, $h) {
    $s.loading = false;
    $s.surveys = {};
    $s.formEnviar={}

    $s.getSurvey = function() {
        var data = {
            opcion: 1
        }
        $h({
            method: 'GET',
            url: '/survey/',
            params: data
        }).then(function successCallback(response) {
            var data = JSON.parse(response.data.message)
            console.log(data)
            $s.surveys = data;
            $s.loading = false;
        }, function errorCallback(response) {
            $s.loading = false;
        });
    }
    $s.getSurvey();

    $s.deleteSurvey = function(id) {
        var data = {
            encuesta: id
        }
        console.log(data)
        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/deleteQuestion/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)
                alert("Se borro correctamente");
                $s.getSurvey();
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }
    $s.encuesta=-1;

    $s.modalEnviar=function(encuesta){
        console.log(encuesta)
        $s.formEnviar.encuesta=encuesta
        $("#modalEnviar").modal()
    }

    $s.enviar=function(){
        var data=$s.formEnviar;
        console.log($s.formEnviar);
        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/enviar/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)
                alert("La encuesta se ha enviado correctamente!")
                $("#modalEnviar").modal("toggle")
               
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
        
    }

}]);

app.controller('answersController', ['$scope', '$http', function($s, $h) {

    $s.answers = {}


    $s.init = function(surveyId) {
        var data = {
            encuesta: surveyId,
        }
        $h({
            method: 'GET',
            url: '/saveAnswer/',
            params: data
        }).then(function successCallback(response) {
            var data = response.data.message
            console.log(data)

            for (var i in data) {
                var labels = []
                var datos=[]
                for (var j of data[i].respuestas) {
                    labels.push(j.respuesta)
                    datos.push(j.numero)
                }
                data[i].labels=labels;
                data[i].data=datos;
                data[i].chart="bar";
            }
            console.log(data)
            $s.answers = data;

        }, function errorCallback(response) {
            $s.loading = false;
        });
    }

    console.log($s.answers)
}]);

app.controller('viewerController', ['$scope', '$http', function($s, $h) {
    $s.form={}
    $s.survey = {}
    $s.currentPage = 0;
    $s.init = function(surveyId) {
        console.log(surveyId)
        var data = {
            id: surveyId,
            opcion: 2
        }
        $h({
            method: 'GET',
            url: '/survey/',
            params: data
        }).then(function successCallback(response) {
            var data = JSON.parse(response.data.message)
            console.log(data)
            var estructura = JSON.parse(data[0].fields.estructura)
            console.log(estructura)
            $s.survey = estructura;

        }, function errorCallback(response) {
            $s.loading = false;
        });
    }
    $s.data={}
    $s.siguiente = function() {
        $s.currentPage += 1;
    }
    $s.atras = function() {
        $s.currentPage -= 1;
    }
    $s.finalizar = function() {
        var data=jQuery('#formulario').serializeArray();
        console.log(data);
        var index=data.length-1;
        $s.guardar(data,index)
        
    }
    $s.guardar=function(respuestas,index){
        var alumno=document.getElementById('alumno').value;
        var data=respuestas[index]
        data.alumno=alumno;
        console.log(data)
        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/guardarRespuesta/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)
               
                if (index > 0) {
                    $s.guardar(respuestas, index - 1)
                } else {
                    alert("La encuesta se guardo correctamente")
                    location.reload();
                }
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }
    console.log($s.survey)
}]);

app.controller('egresadoController', ['$scope', '$http', function($s, $h) {
    $s.alumnos=[];
    $s.formAddAlumno={}
    $s.formCarrera={}
    
    

    $s.obtenerAlumnos=function(id){

        console.log(id)
        var data = {
            carrera: id,
        }
        console.log(data)
        $h({
            method: 'GET',
            url: '/getAlumnos/',
            params: data
        }).then(function successCallback(response) {
            var data = JSON.parse(response.data.message)
            console.log(data)
            $s.alumnos=data;
            $("#modalAlumno").modal();

        }, function errorCallback(response) {
            $s.loading = false;
        });
        

    }
    $s.abrirModalAddAl=function(carrera){
        console.log(carrera)
        $s.formAddAlumno.carrera=carrera;
        $("#modalAgregarAlumno").modal();
    }

    $s.agregarAlumno=function(){
        console.log("datos",$s.formAddAlumno);
        var data=$s.formAddAlumno;
        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/getAlumnos/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)
               
                alert("El alumno se agrego correctamente")
                location.reload();
                
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }

    $s.agregarCarrera=function(){
        console.log("datos",$s.formCarrera);
        var data=$s.formCarrera;
        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/guardarCarrera/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)
               
                alert("La carrera se agrego correctamente")
                location.reload();
                
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }

    $s.init = function(surveyId) {
        var data = {
            id: surveyId,
            opcion: 2
        }
        $h({
            method: 'GET',
            url: '/survey/',
            params: data
        }).then(function successCallback(response) {
            var data = JSON.parse(response.data.message)
            console.log(data)
            var estructura = JSON.parse(data[0].fields.estructura)
            console.log(estructura)
            $s.survey = estructura;

        }, function errorCallback(response) {
            $s.loading = false;
        });
    }

}]);

app.controller('builder', ['$scope', function($s) {
    $s.menu = 2;
    $s.survey = { id: "", name: "", description: "", pages: [{ page: 1, questions: [] }] };
    $s.currentPage = 1;
    $s.indexPage = 1;
    $s.currentQuestion = 1;
    $s.addPage = function() {
        var flag = false;
        for (var page of $s.survey.pages) {
            if (page.questions.length == 0) {
                alert("Page " + page.page + " is empty");
                flag = true;
                break;
            }
            for (var question of page.questions) {
                if (question.description == "") {
                    alert("Question " + question.question + " is empty")
                    flag = true;
                    break;
                }
            }
        }

        if (flag) {
            return
        }

        if ($s.indexPage == 5) {
            alert("The max page number is 5")
            return
        }
        $s.indexPage++;
        $s.survey.pages.push({ page: $s.indexPage, questions: [] })
        $s.currentPage++;
    }
    $s.changePage = function(page) {
        $s.currentPage = page;
    }

    $s.refresh = function() {
        $s.survey = { id: "", name: "", description: "", pages: [{ page: 1, questions: [] }] };
    }

    $s.add = function(type) {

        var id = ((+new Date) * Math.random()).toString(36);

        var question = { id: id, question: $s.currentQuestion, description: "", type: type, required: true, option: [] };
        if (type == 1) {

            question.multiselect = false;
            question.option.push({ value: '' ,id:((+new Date) * Math.random()).toString(36)})
            question.option.push({ value: '' ,id:((+new Date) * Math.random()).toString(36)})
            question.option.push({ value: '' ,id:((+new Date) * Math.random()).toString(36)})
            

        } else if (type == 2) {

        } else if (type == 3) {
            question.max = 10;
            question.min = 0;

        } else if (type == 4) {
            question.option.push({ value: 'Yes',id:((+new Date) * Math.random()).toString(36)})
            question.option.push({ value: 'No', id:((+new Date) * Math.random()).toString(36)})
        }
        $s.currentQuestion += 1;
        $s.survey.pages[$s.currentPage - 1].questions.push(question);
    }

    $s.remove = function(index) {
        console.log(index);
        if (index == 0 && $s.survey.pages[$s.currentPage - 1].questions.length == 1)
            $s.survey.pages[$s.currentPage - 1].questions = [];
        else
            $s.survey.pages[$s.currentPage - 1].questions.splice(index, 1);
    }

    $s.removeOption = function(question, index) {
        console.log(question, index)
        question.option.splice(index, 1)
    }

    $s.addOption = function(question) {
        console.log(question)
        question.option.push({ value: '' ,id:((+new Date) * Math.random()).toString(36)})
    }

    $s.clone = function(element) {
        var copy = angular.copy(element)
        var id = ((+new Date) * Math.random()).toString(36);
        copy.id = id;
        $s.survey.pages[$s.currentPage - 1].questions.push(copy);
    }

    $s.save = function() {
        var data = {
            nombre: $s.survey.name,
            descripcion: $s.survey.description,
            estructura: JSON.stringify($s.survey)
        }
        console.log(data)

        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/survey/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)
                if (data.error == 1) {
                    var pages = $s.survey.pages;
                    var index = $s.survey.pages.length;
                    $s.pagesIteration(pages, index - 1, data.encuesta)
                }
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }
    $s.pagesIteration = function(pages, index, encuesta) {
        console.log(pages)
        var questions = pages[index].questions;
        console.log("questions", questions)
        var indexQuestions = questions.length;
        console.log("indexQuestions", indexQuestions)
        $s.saveQuestion(questions, indexQuestions - 1, encuesta);
        if (index > 0) {
            $s.pagesIteration(pages, index - 1, encuesta);
        }
    }

    $s.saveQuestion = function(questions, index, encuesta) {
        console.log(questions, index)
        var question = questions[index]
        var data = {
            tipo: question.type,
            descripcion: question.description,
            encuesta: encuesta,
            json_id:question.id
        }
        console.log(data, index)

        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/saveQuestion/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)
                //Guardando posibles Respuestas
                if (question.type == 1) {
                    var indexA = question.option.length - 1;
                    var answer = question.option;
                    $s.saveAnswer(answer, indexA, data.pregunta);
                }

                if (index > 0) {
                    $s.saveQuestion(questions, index - 1, encuesta)
                } else {
                    alert("La encuesta se guardo correctamente")
                    location.reload();
                }
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }

    $s.saveAnswer = function(answers, index, preguntaId) {
        console.log(answers)
        var answer = answers[index]
        var data = {
            valor: answer.value,
            pregunta: preguntaId,
            json_id:answer.id
        }
        console.log(data)
        var token = document.getElementById('token').value;
        $.ajax({
            type: "POST",
            url: "/saveAnswer/",
            headers: { "X-CSRFToken": token },
            data: data,
            dataType: "json",
            success: function(data) {
                console.log(data)

                if (index > 0) {
                    $s.saveAnswer(answers, index - 1, preguntaId)
                }
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });

    }

}]);