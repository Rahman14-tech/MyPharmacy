document.addEventListener('DOMContentLoaded',()=>{
    let minus = document.querySelector('#minus_barang');
    let choice = document.querySelector('#input_barang_masuk');
    let plus = document.querySelector('#plus_barang');
    let stock = document.querySelector('#the_stok');
    minus.addEventListener('click',()=>{
        let choicetemp = Number(choice.value);
        if(choicetemp > 0){
            choicetemp-=1;
        }   
        choice.value = String(choicetemp);
    })
    plus.addEventListener('click',()=>{
        let choicetemp = Number(choice.value);
        let tempstock = Number(stock.innerHTML);
        if(choicetemp < tempstock){
            choicetemp+=1;
        }
        choice.value = String(choicetemp);
    })
})