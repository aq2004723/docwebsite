{% extends "base.html" %} 
{% block mainpage %}
    <div  class="container marketing" id="docresult">
      <!-- Three columns of text below the carousel -->
      <div class="row" >
        {% for doc in docs %}
            {% module docModule(doc) %}
        {% end %}
      </div><!-- /.row -->
      <hr class="featurette-divider">
{% end %}

{% block modal %}
  {% for doc in docs %}
    {% module showdocModule(doc) %}
  {% end %}
{% end %}

{% block otherjs%}
  <script type="text/javascript">
    window.onload = function (){
      {% for doc in docs %}
        var temp{{doc.get('_id')}} = new PDFObject({ url:"{{doc.get('pdflocation')}}" }).embed("{{doc.get('_id')}}show");
      {% end %}
    };
  </script>
{% end %}

