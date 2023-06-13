/**
 * 
 */
	//var flag="true";
	
	function loadhome() {
		$('#maincontent').load("pages/home.html");
	};	
	
	function loadsearch() {
		$('#maincontent').load("pages/search.html");
	};	
	
	function loadlookup() {	
		$('#maincontent').load("pages/lookup.html");	
	};
	
	function loadexplore() {	
		$('#maincontent').load("pages/explore.html");	
	};
	
	function loadmap() {
		$('#maincontent').load("pages/map.html");
	};
	
	function loaddisb() {
		$('#maincontent').load("pages/disb.html");
	};	
	
	function loadvalidation() {
		$('#maincontent').load("pages/validate.html");
	};	
	
	function loadcreateDB() {
		if(true==checkHostname())
			$('#maincontent').load("pages/dbconfig.html");
	};	

	function loadsublicence() {	
		$('#maincontent').load("pages/sublicense.html");
	//	$('#maincontent').unload("pages/sublicense.html");
	
		
	};
	function closesublicens(){
		$('#sublicenceid').css('padding-right','75%');		
		$('#sublicenseclose').css('width','0px');	
		var getUrl=window.location;
			getUrl.reload()
			
			
		}
	

	function loadparameterbar() {		
		$('#maindiv').css('padding-left','0px');		
		$('#parametersidenav').css('width','30%');
		
	};

	function closeparameterbar(){		
		$('#maindiv').css('padding-left','15%');		
		$('#parametersidenav').css('width','0px');	
		
	};
	
	$(document).ready(function() {
	    // Configure/customize these variables.
	    var showChar = 100;  // How many characters are shown by default
	    var ellipsestext = "...";
	    var moretext = "More >>";
	    var lesstext = "<< Less";
	    
	    

	    $('.more').each(function() {
	        var content = $(this).html();
	 
	        if(content.length > showChar) {
	 
	            var c = content.substr(0, showChar);
	            var h = content.substr(showChar, content.length - showChar);
	 
	            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
	 
	            $(this).html(html);
	        }
	 
	    });
	 
	    $(".morelink").click(function(){
	        if($(this).hasClass("less")) {
	            $(this).removeClass("less");
	            $(this).html(moretext);
	        } else {
	            $(this).addClass("less");
	            $(this).html(lesstext);
	        }
	        $(this).parent().prev().toggle();
	        $(this).prev().toggle();
	        return false;
	    });
	    
	   checkHostname();
	    
	    //if(flag=="true")
	    	checkProperties();
	   
	});
	
	function checkProperties(){
		messageResource.init({
	    	  // path to directory containing config.properties
	    	  filePath : ''
	    	});
	    
	    messageResource.load('system', function(){ 
	    	  // get value corresponding  to a key from system.properties  
	    	  var flagValue = messageResource.get('config.flag', 'system');
	    	  //alert(flagValue);
	    	  if(flagValue=="false"){
	    		  $('#menubar').show();
	    		  $('#maincontent').load("pages/home.html");
	    	  }
	    	  if(flagValue=="true"){
	    		  //flag="false";
	    		  $('#maincontent').load("pages/config.html");
	    		  $('#menubar').hide();
	    	  }
	    	  
	    	}); 
	}

	function checkHostname() {
		if(window.location.hostname!='localhost'){
			$('#configLink').hide();
			return false;
		}			
		else{
			$('#configLink').show();
			return true;
		}
	}
	
	function getAllSemanticTags(){
		var url=window.location.href;
		if(url.charAt(url.length-1)=="#"){
			url=url.substring(0, url.length - 2);	
		}
		document.getElementById("linksemantic").setAttribute("href", url+"/api/search/semantic");
		
	}