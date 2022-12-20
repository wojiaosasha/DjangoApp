function hideAllBlock() {
    document.getElementById("yes").style.display = 'none';
    document.getElementById("no").style.display = 'none';
  }
  
  function Selected(a) {
    hideAllBlock();
    document.getElementById(a.value).style.display = 'block';
  }