// Before trying to sign in a user to ORCID, first verify they're signed out.
var link = $(".connect-orcid-link");
    link.click(function(event) {
        $.ajax({
            url: 'https://sandbox.orcid.org/userStatus.json?logUserOut=true',
            dataType: 'jsonp',
            success: function(result,status,xhr) {
                //pass
            },
            error: function (xhr, status, error) {
                console.log("Failed logging out from ORCID.");
            }
        });
});
