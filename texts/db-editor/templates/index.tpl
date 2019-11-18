<!doctype html>
<html>
<head>
<!-- $Id: index.tpl,v 1.18 2016/12/17 10:16:58 mechanoid Exp $ -->
<title>flask</title>
<meta charset='utf-8'/>
<style>

.class-count {
   border:1px #000 solid;
   padding: 5px;
   display: table;
   margin:0 auto;
}

.class-count table {
   border-spacing: 0;
}

.class-count td {
   border-right:1px #000 solid;
   border-bottom:1px #000 solid;
   padding: 5px 10px;
   text-align:center;
}
.class-count td:last-child {
   border-right:0
}
.class-count tr:last-child td {
   border-bottom:0;
}

hr {
   border-bottom:1px #000 solid;
}

.article {
   border-bottom:2px #000 solid;
   padding: 20px 50px;
}

.article:first-child {
   border-top:2px #000 solid;
}

.tool-button {
   margin: 0 5px;
}

.form-paginator input[type="text"] {
   border:1px #000 solid;
   text-align:center;
}

.form-data textarea {
   width:100%;
   height:200px;
   resize: none;
   border:1px #000 solid;
   font-size:11pt;
   background-color:#eee;
}

.bar {
   background-color:#0ff;
   border-top:1px #00f solid;
   float:right;
}
.bar-frame {
   border:1px #000 solid;
   height:100px;
}


</style>
</head>
<body>

<form id='form_paginator3' class='form-paginator'  action="/" method="GET">
   БД : <a href="/">{{ dbname }}</a> &nbsp; &nbsp;| &nbsp; &nbsp;всего записей: {{ rec_numb }} &nbsp; &nbsp;|&nbsp; &nbsp;
   записей на страницу: 
   <input type="text" name='size' size=4  value="{{ size }}" onkeypress="return only_digits_validator(event,this.form);"  /> 
   &nbsp; &nbsp;| &nbsp; &nbsp; фильтр:
   <select name="filt_tag" onchange="this.form.submit();" title='фильтр по классу текста'>
      <option> - </option>
      {% for t in tags %}
	 {% if t == filt_tag %}
	    <option selected=1>{{ t }}</option>
	 {% else %}
	    <option>{{ t }}</option>
	 {% endif %}
      {% endfor %}
   </select>
</form>
<hr/>
<p/>


<input type="hidden" id='maxpage' name='maxpage' value="{{ maxpage }}" /> 
&nbsp;
<p/>
<center>
<form id='form_paginator1' class='form-paginator'  action="/" method="GET">
   страница:  
   <input type='button' {% if page == 1 %} disabled {% endif %} value='<<' onclick="return button_first_pressed(event,this.form);" title='первая страница'/> 
   <input type='button' {% if page == 1 %} disabled {% endif %} value='<'  onclick="return button_backward_pressed(event,this.form);" title='предыдущая страница'/> 

   &nbsp;&nbsp;
   <input type="text"   name='page' size=4  value="{{page}}" onkeypress="return only_digits_validator(event,this.form);" /> 
   / {{ maxpage }}&nbsp;&nbsp;
   <input type='button' {% if page == maxpage %} disabled {% endif %} value='>'  onclick="return button_forward_pressed(event,this.form);" title='следующая страница'/>
   <input type='button' {% if page == maxpage %} disabled {% endif %} value='>>' onclick="return button_last_pressed(event,this.form);" title='последняя страница' /> 
   <input type="hidden" name='size' value="{{ size }}" />
   <input type="hidden" name='filt_tag' value="{{ filt_tag }}"/>
</form>
</center>

<p/>
<hr/>

{% for num in range(text|count) %}
<div class="article">
      <form  action="/" method="POST" class="form-data">
        запись: {{ num+((page-1)*size)+1 }} &nbsp;&nbsp; | &nbsp;&nbsp;
	 id: {{  text_id[num] }}<p/> 
	 <textarea name="text" onkeypress="this.style.backgroundColor='#cf0';this.form.elements['tag'].disabled=true;this.form.elements['button_save'].disabled=false;">{{  text[num] }}</textarea>
	 <p/> 
	 класс: <select name="tag" onchange="return select_class_changed(event,this.form);" title='изменить класс текста'>
	    {% for t in tags %}
	       {% if t == tag[num] %}
		  <option selected=1>{{ t }}</option>
	       {% else %}
		  <option>{{ t }}</option>
	       {% endif %}
	    {% endfor %}
	 </select>
	 &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;
	 <input type='button' class='tool-button' name='button_save' value='сохранить' disabled=1 title='сохранить изменения текста' onclick="return button_edit_pressed(event,this.form);"/>
	 <input type='button' class='tool-button' value='удалить' title='удалить запись'  onclick="return button_delete_pressed(event,this.form);"/>

	 <input type='hidden' name='action' value="none" />
	 <input type='hidden' name='text_id' value="{{  text_id[num] }}" />
	 <input type='hidden' name='page' value="{{ page }}" />
	 <input type='hidden' name='size' value="{{ size }}" />
	 <input type="hidden" name='filt_tag' value="{{ filt_tag }}"/>
      </form>
</div>
{% endfor %}

<p/>

<center>
<form id='form_paginator2' class='form-paginator'  action="/" method="GET">
 страница:  
   <input type='button' {% if page == 1 %} disabled {% endif %} value='<<' onclick="return button_first_pressed(event,this.form);" title='первая страница'/> 
   <input type='button' {% if page == 1 %} disabled {% endif %} value='<' onclick="return button_backward_pressed(event,this.form);" title='предыдущая страница'/> 
   &nbsp;&nbsp;
   <input type="text"   name='page' size=4  value="{{page}}" onkeypress="return only_digits_validator(event,this.form);" /> 
   / {{ maxpage }}&nbsp;&nbsp;
   <input type='button' {% if page == maxpage %} disabled {% endif %} value='>' onclick="return button_forward_pressed(event,this.form);" title='следующая страница'/>
   <input type='button' {% if page == maxpage %} disabled {% endif %} value='>>' onclick="return button_last_pressed(event,this.form);" title='последняя страница' /> 
   <input type="hidden" name='size' value="{{ size }}" />
   <input type="hidden" name='filt_tag' value="{{ filt_tag }}"/>
</form>
</center>

<p/>
   <div class='class-count'>
   всего записей: {{ rec_numb }}<p/>
   <table>
   <tr>{% for t in tags %} <td> {{ t }} </td>{% endfor %} </tr>
   <tr>{% for t in tags %} <td>{{ tags[t] }} </td>{% endfor %} </tr>
   </table>
</div><!-- class-count -->

<p/>
<script>
only_digits_validator = function(e,form) {
   e = e || window.event; 
   if (e.keyCode == 13) { form.submit() ; }
   k = [8,46,37,39]; 
   return (k.indexOf(e.keyCode) !== -1) || (e.charCode >= 48 && e.charCode <= 57);
}

button_forward_pressed = function(e,form) {
   maxpage = parseInt(document.getElementById('maxpage').value) ;
   page = parseInt(form.elements['page'].value) ; 
   if(page < maxpage) { 
      form.elements['page'].value = page + 1.0 ; 
      form.submit() ; 
   }
   return true;
}

button_backward_pressed = function(e,form) {
   page = parseInt(form.elements['page'].value) ; 
   if (page > 1) {
      form.elements['page'].value = page - 1.0 ; 
      form.submit() ;
   }
   return true;
}

button_first_pressed = function(e,form) {
   if ( parseInt(form.elements['page'].value) < 2 ) { return true; } 
   form.elements['page'].value = 1; 
   form.submit() ; 
   return true;
}

button_last_pressed = function(e,form) {
   if ( parseInt(form.elements['page'].value) >= parseInt(document.getElementById('maxpage').value)  ) { return true; } 
   form.elements['page'].value =  document.getElementById('maxpage').value ; 
   form.submit() ; 
   return true;
}

button_delete_pressed = function(e,form) {
   e = e || window.event; 

   if(!confirm('удалить?')) return false;
   form.elements['action'].value = 'delete' ;
   form.submit(); 
   return true;
}

select_class_changed = function(e,form) {
   e = e || window.event; 
   /* if(!confirm('изменить класс?')) return false; */
   form.elements['action'].value = 'tag' ;
   form.submit(); 
   return true;
}

button_edit_pressed = function(e,form) {
   e = e || window.event; 
   form.elements['action'].value = 'text' ;
   form.submit(); 
   return true;
}

</script>



</body>
</html>


