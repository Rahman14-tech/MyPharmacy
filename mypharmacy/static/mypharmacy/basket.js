addEventListener('DOMContentLoaded',()=>{
    let property = document.querySelectorAll('.buttontrans')
    let property1 = document.querySelectorAll('.buttontrans')
    let theTotal = document.querySelector('#theTotal')
    if(property !== null){
        for(let i=0;i<property.length;i++){
            let theparentId = `detailBarang${property[i].id}`
            const parentObject = document.querySelector(`#${theparentId}`)
            property[i].addEventListener('click',()=>{
                let thetotalInt = parseInt(theTotal.innerHTML)
                let origin = parseInt(property[i].value)
                let realtotal = thetotalInt - origin
                theTotal.innerHTML = realtotal
                fetch('http://127.0.0.1:8000/f742cf2703e3300ef932616cd5fe0541',{
                    method:'PUT',
                    body:JSON.stringify({
                        propertyId:property[i].id,
                    })
                })
                .then(response => response.json())
                .then(result =>{
                    parentObject.style.animationPlayState = 'running';
                    parentObject.addEventListener('animationend',()=>{
                        parentObject.remove()
                    })
                })
            })
        }
    }
})