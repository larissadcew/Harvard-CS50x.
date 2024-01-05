//Run script once DOM is loded
document.addEventListener('DOMContentLoaded',function(){

    let correct = document.querySelector('.correct');
    correct.addEventListener('click', function(){
        correct.style.backgroundColor = 'green';
        document.querySelector('#feedback1').innerHTML = ' correct!';

    });
    let incorrects = document.querySelectorAll('.incorrect');
    for(let i = 0;i < incorrects.length; i++){
        incorrects[i].addEventListener('click',function(){
            incorrects[i].style.backgroundColor = 'red';
            document.querySelector('#feedback1').innerHTML = 'Incorrect';

        });
    }
   document.querySelector('#buttonIN').addEventListener('click', function(){
    let input = document.querySelector('#answer');
    if(input.value === 'Stan Pines'){
        input.style.backgroundColor = 'green';
        document.querySelector('#feedback2').innerHTML = 'Correct';
    }else{
        input.style.backgroundColor = 'red';
        document.querySelector('#feedback2').innerHTML = 'Incorrect';
    }
   });
  });