ROUTER.registerController('userspace:editor:form', {
  init: function() {
    var journals = $('#id_editor_form_metadata').data('journals');
    function resetContactField() {
      $("#id_contact").val("");
      $("#id_contact").find("option").hide();
    }

    resetContactField();
    $("#id_journal").change(function(){
      var journal_id = $(this).val();
      var members = journals[journal_id];
      resetContactField();
      for (len = members.length, i=0; i<len; ++i) {
        $("#id_contact").find("option[value='"+members[i]+"']").show();
      }
    });

    function checkUploads(ev) {
      var filesAddedCount = $('#id_submissions').data('files-added');
      var filesUploadingCount = $('#id_submissions').data('files-uploading');
      if (!filesAddedCount && !filesUploadingCount) {
        return;
      }

      if(filesAddedCount) {
        r = confirm(gettext("Certains de vos fichiers n'ont pas étés téléversés. Êtes-vous sûr ?"));
        if (r == true) { return; }
      }

      if(filesUploadingCount) {
        r = confirm(gettext("Certains de vos fichiers ne sont pas complètement téléversés. Êtes-vous sûr ?"));
        if (r == true) { return; }
      }

      ev.preventDefault();
    }

    $('form').submit(checkUploads);
    $('a:not(form a)').click(checkUploads);
    window.onbeforeunload = checkUploads;
  },
});
