  var mode = 'c';
	var cEditor = CodeMirror.fromTextArea(document.getElementById("c-code"), {
        lineNumbers: true,
        theme: "monokai",
        autoCloseBrackets: true,
        keyMap: "sublime",
        matchBrackets: true,
        showCursorWhenSelecting: true,
        mode: 'text/x-csrc',
        extraKeys: {
        "F11": function(cm) {
          cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        "Esc": function(cm) {
          if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        }
      }
    });
  function downloadCode(){
    var text = cEditor.getValue();
    var filename = 'solution.'+mode;
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);
    pom.click();
  }
  function onFileSelected(event) {
    var selectedFile = event.target.files[0];
    var reader = new FileReader();
    var result = document.getElementById("result");
    reader.onload = function(event) {
      cEditor.getDoc().setValue(event.target.result);
    };
    reader.readAsText(selectedFile);
  }
  var input = document.getElementById("selectt");
  function selectTheme() {
    var theme = input.options[input.selectedIndex].innerHTML;
    cEditor.setOption("theme", theme);
  }
  var choice = document.location.search &&
               decodeURIComponent(document.location.search.slice(1));
  if (choice) {
    input.value = choice;
    cEditor.setOption("theme", choice);
  }
  var modeInput = document.getElementById("selectl");
  function selectMode() {
    var myindex  = modeInput.selectedIndex;
    var modefly = modeInput.options[myindex].text.toLowerCase();
    //alert(modefly);
    if(modefly=="c"){
      cEditor.setOption("mode", 'text/x-csrc');
      mode="c";
    }
    else if(modefly=="c++"){
      cEditor.setOption("mode", 'text/x-c++src');
      mode="cpp";
    }
    else if(modefly=="java"){
      cEditor.setOption("mode", 'text/x-java');
      mode="java";
    }
    else if(modefly=="python"){
      cEditor.setOption("mode", 'text/x-python');
      mode="py";
    }
    else if(modefly=="javascript"){
      cEditor.setOption("mode", 'text/javascript');
      mode="js";
    }
    else if(modefly=="go"){
      cEditor.setOption("mode", 'text/x-go');
      mode="go";
    }
    else
      cEditor.setOption("mode", 'text/x-csrc');
   }
