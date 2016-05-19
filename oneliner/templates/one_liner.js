(function() {
  var services = [
  {% for service in services %}{{ service|safe }}{% if not forloop.last %},
  {% endif %}{% endfor %}
  ];

  var load_google_analytics = function(service) {
    window['GoogleAnalyticsObject'] = 'ga';
    window.ga = window.ga || function(){
      (ga.q=ga.q||[]).push(arguments);
    };
    ga.l =+ new Date;

    var scriptEl = document.createElement('script');
    scriptEl.async = 1;
    scriptEl.src = 'https://www.google-analytics.com/analytics.js';

    var firstScriptEl = document.getElementsByTagName('script')[0];
    firstScriptEl.parentNode.insertBefore(scriptEl, firstScriptEl);

    ga('create', service.account_id, 'auto');
    ga('send', 'pageview');

    return false;
  };

  var load_chartbeat = function(service) {
    var parser = document.createElement('a');
    parser.href = service.organization.url;

    var _sf_async_config = { uid: service.account_id, domain: parser.hostname, useCanonical: true };
    (function() {
      function loadChartbeat() {
        window._sf_endpt = (new Date()).getTime();
        var e = document.createElement('script');
        e.setAttribute('language', 'javascript');
        e.setAttribute('type', 'text/javascript');
        e.setAttribute('src','//static.chartbeat.com/js/chartbeat.js');
        document.body.appendChild(e);
      };
      var oldonload = window.onload;
      window.onload = (typeof window.onload != 'function') ?
        loadChartbeat : function() { oldonload(); loadChartbeat(); };
    })();
  };

  for (idx in services) {
    // TODO: Use "callback" field from django model to determine which function loads the service
    if (services[idx].type == 'Chartbeat') {
      load_chartbeat(services[idx]);
    }
    if (services[idx].type == 'Google Analytics') {
      load_google_analytics(services[idx]);
    }
  }
})();
