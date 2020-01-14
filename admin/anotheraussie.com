<!-- START Main Content -->
<div class="row-fluid"> 
<!-- START Tabbed Content -->
	<ul class="nav nav-tabs" id="myTab">
	  <li class="active"><a href="#pending">Pending</a></li>
	  <li><a href="#complete">Complete</a></li>
	  <li><a href="#archive">Archive</a></li>
	</ul>

<div class="tab-content"> 
  <div class="tab-pane active" id="pending">
    <div class="span8 well"> <!-- START Main Form -->
      <legend>Create New Job - New Customer 
      </legend>
    </div>

    <form>
 <!-- <legend> Create New Service Job</legend>-->

    <div class="row-fluid">  <!--First Row -->
      <div class="span3">
        <label>First Name</label>
	<input type="text" class="span12" id="input01">
      </div>

      <div class="span3">
        <label>Last Name</label>
	<input type="text" class="span12" id="input01">
      </div>

      <div class="span3">
        <label>Location</label>
	<div class="btn-group">
          <button class="btn">Action </button>
	  <button class="btn dropdown-toggle" data-toggle="dropdown"> <span class="caret"></span>
        </div>
      </div> <!-- class="span3" -->
    </div> <!-- /First Row -->

    <div class="row-fluid">   <!--2nd Row -->
      <div class="span6">
	<div class="control-group">
          <label class="control-label" for="textarea">Job Description</label>
          <div class="controls">
            <textarea class="input-xlarge span12" id="textarea" rows="3"></textarea>
          </div>
        </div> <!-- /control-group -->      
      </div> <!-- /span6 -->

      <div class="span3">
        <label>Text 1</label>
	<input type="text" class="span3" id="input01">
      </div>
 
      <div class="span3">
        <label>Text 2</label>
	<input type="text" class="span3" id="input01">
      </div>
    </div> <!-- /2nd Row -->
  </form>
	
</div> <!-- END Main Content -->

</div>  
<!-- END Main Container -->       
