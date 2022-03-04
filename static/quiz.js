console.log('hello world quiz')
const quizBox = document.getElementById('quiz-box')     // insert questions and answers to line 101 of quiz_form.html
const url = window.location.href
let quiz_data



$.ajax({
    type: 'GET',
    url: `${url}data`,        // get dictionary created from JsonResponse in quiz_data_view in views.py
    success: function(response){
        console.log(response)
        data = response.quiz_data    // get every element of quiz and answers from dictionary
        data.forEach(el => {        // to loop each question from the dictionary to take quiz page
            for (const [question, answers] of Object.entries(el)){
                quizBox.innerHTML += `
                    <br>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `

                answers.forEach(answer => {     // to loop each answer from the dictionary to take quiz page
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                        <hr>
                    `
                })
            }
        });
    },
    error: function(error){
        console.log(error)
    }
})

const quizForm =  document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            // console.log(response)
            const results = response.results
            console.log(results)
        },
        error: function(error){
            console.log(error)
        }

    })

}

quizForm.addEventListener('submit', e=>{
    e.preventDefault()

    sendData()
})