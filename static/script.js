//дожидаемся полной загрузки страницы
window.onload = function () {
    //ищем элемент по селектору
    var a = document.querySelector('#ShowHide1');
    var b = document.querySelector('#ShowHide2');
    var c = document.querySelector('#ShowHide3');
    var d = document.querySelector('#ShowHide4');
    var f = document.querySelector('#ShowHide5');
    var g = document.querySelector('#ShowHide6');
    var h = document.querySelector('#ShowHide7');
    var i = document.querySelector('#ShowHide8');
    var k = document.querySelector('#ShowHide9');
    let timeout=2000;
    //вешаем на него события
    a.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple1').style.display='none',timeout);}
    b.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple2').style.display='none',timeout); }
    c.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple3').style.display='none',timeout); }
    d.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple4').style.display='none',timeout);}
    f.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple5').style.display='none',timeout); }
    g.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple6').style.display='none',timeout); }
    h.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple7').style.display='none',timeout);}
    i.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple8').style.display='none',timeout); }
    k.onmouseout = function(e) {
      setTimeout(()=>document.getElementById('exemple9').style.display='none',timeout); }
    a.onmouseover = function(e) {
      document.getElementById('exemple1').style.display='block'; };
    b.onmouseover = function(e) {
      document.getElementById('exemple2').style.display='block';};
    c.onmouseover = function(e) {
      document.getElementById('exemple3').style.display='block'; };
    d.onmouseover = function(e) {
      document.getElementById('exemple4').style.display='block'; };
    f.onmouseover = function(e) {
      document.getElementById('exemple5').style.display='block';};
    g.onmouseover = function(e) {
      document.getElementById('exemple6').style.display='block'; };
    h.onmouseover = function(e) {
      document.getElementById('exemple7').style.display='block'; };
    i.onmouseover = function(e) {
      document.getElementById('exemple8').style.display='block';};
    k.onmouseover = function(e) {
      document.getElementById('exemple9').style.display='block'; };
  }
      