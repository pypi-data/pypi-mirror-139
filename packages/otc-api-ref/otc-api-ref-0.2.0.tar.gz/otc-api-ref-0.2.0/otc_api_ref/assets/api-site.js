/*
(function() {
    // the list of expanded element ids
    var expanded = [];
    // whether we should sync expand changes with the location
    // url. We need to make this false during large scale
    // operations because we're using the history API, which is
    // expensive. So a bulk expand turns this off, expands
    // everything, turns it back on, then does a history sync.
    var should_sync = true;

    $(document).ready(function() {
        // Expand the world. Wires up the expand all button, it turns
        // off the sync while it is running to save the costs with the
        // history API.
        var expandAllActive = true;
        $('#expand-all').click(function () {
            should_sync = false;
            if (expandAllActive) {
                expandAllActive = false;
                $('.api-detail').collapse('show');
                $('#expand-all').attr('data-toggle', '');
                $(this).text('Hide All');
            } else {
                expandAllActive = true;
                $('.api-detail').collapse('hide');
                $('#expand-all').attr('data-toggle', 'collapse');
                $(this).text('Show All');
            }
            should_sync = true;
            sync_expanded();
        });

        // if there is an expanded parameter passed in a url, we run
        // through and expand all the appropriate things.
        if (window.location.search.substring(1).indexOf("expanded") > -1) {
            should_sync = false;
            var parts = window.location.search.substring(1).split('&');
            for (var i = 0; i < parts.length; i++) {
                var keyval = parts[i].split('=');
                if (keyval[0] == "expanded" && keyval[1]) {
                    var expanded_ids = keyval[1].split(',');
                    for (var j = 0; j < expanded_ids.length; j++) {
                        $('#' + expanded_ids[j]).collapse('show');
                    }
                }
            }
            should_sync = true;
            // This is needed because the hash *might* be inside a
            // collapsed section.
            //
            // NOTE(sdague): this doesn't quite seem to work while
            // we're changing the rest of the document.
            $(document.body).scrollTop($(window.location.hash).offset().top);
        }

        // Wire up microversion selector
        $('.mv_selector').on('click', function(e) {
            var version = e.currentTarget.innerHTML;
            // flip what is active
            $(this).addClass('active').siblings().removeClass('active');
            if (version == "All") {
                reset_microversion();
            } else {
                set_microversion(version);
            }
        });
    });
    / **
     * Helper function for setting the text, styles for expandos
     * /
    function processButton(button, text) {
        $('#' + $(button).attr('id') + '-btn').text(text)
            .toggleClass('btn-info')
            .toggleClass('btn-default');
    }

    // Take the expanded array and push it into history. Because
    // sphinx is building css appropriate ids, they should not have
    // any special characters we need to encode. So we can simply join
    // them into a comma separated list.
    function sync_expanded() {
        if (should_sync) {
            var url = UpdateQueryString('expanded', expanded.join(','));
            history.pushState('', 'new expand', url);
        }
    }


})();
*/
