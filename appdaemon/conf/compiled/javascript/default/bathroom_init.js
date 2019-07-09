$(function(){ //DOM Ready

    function navigate(url)
    {
        window.location.href = url;
    }

    $(document).attr("title", "Bathroom");
    content_width = (120 + 5) * 5 + 5
    $('.gridster').width(content_width)
    $(".gridster ul").gridster({
        widget_margins: [5, 5],
        widget_base_dimensions: [120, 120],
        avoid_overlapped_widgets: true,
        max_rows: 15,
        max_size_x: 5,
        shift_widgets_up: false
    }).data('gridster').disable();
    
    // Add Widgets

    var gridster = $(".gridster ul").gridster().data('gridster');
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baselight-default-lights" id="default-lights"><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><span class="toggle-area" id="switch"></span><p class="state_text" data-bind="text: state_text, attr:{style: state_text_style}"></p><div class="levelunit"><p class="level" data-bind="text: level, attr:{style: level_style}"></p><p class="unit" data-bind="html: units, attr:{style: unit_style}"></p></div><p class="secondary-icon minus"><i data-bind="attr: {class: icon_down, style: level_down_style}" id="level-down"></i></p><p class="secondary-icon plus"><i data-bind="attr: {class: icon_up, style: level_up_style}" id="level-up"></i></p></div></li>', 1, 1, 1, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-getting-ready" id="default-getting-ready"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 2, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-fluxer" id="default-fluxer"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 3, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basemedia-default-speaker" id="default-speaker"><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="artist" data-bind="text: artist, attr:{style: artist_style}"></h1><h1 class="media_title" data-bind="text: media_title, attr:{style: media_title_style}"></h1><h1 class="album" data-bind="text: album, attr:{style: album_style}"></h1><h2 id="previous" class="previous" data-bind="attr:{style: previous_icon_style}"><i data-bind="attr: {class: previous_icon}"></i></h2><h2 id="play" class="play" data-bind="attr:{style: play_icon_style}"><i data-bind="attr: {class: play_icon}"></i></h2><h2 id="next" class="next" data-bind="attr:{style: next_icon_style}"><i data-bind="attr: {class: next_icon}"></i></h2><p class="state_text" data-bind="text: state_text, attr:{style: state_text_style}"></p><div class="levelunit"><p class="level" data-bind="text: level, attr:{style: level_style}"></p><p class="unit" data-bind="attr:{style: units_style}">%</p></div><p class="secondary-icon minus"><i data-bind="attr: {class: icon_down, style: level_down_style}" id="level-down"></i></p><p class="secondary-icon plus"><i data-bind="attr: {class: icon_up, style: level_up_style}" id="level-up"></i></p></div></li>', 2, 2, 4, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-fan" id="default-fan"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 1, 2)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-wake-up" id="default-wake-up"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 2, 2)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseswitch-default-motion" id="default-motion"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 3, 2)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-temperature" id="default-temperature"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 4, 3)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-humidity" id="default-humidity"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 5, 3)
    
    
    
    var widgets = {}
    // Initialize Widgets
    
        widgets["default-lights"] = new baselight("default-lights", "", "default", {'widget_type': 'baselight', 'entity': 'light.bathroom', 'post_service_active': {'service': 'homeassistant/turn_on', 'entity_id': 'light.bathroom'}, 'post_service_inactive': {'service': 'homeassistant/turn_off', 'entity_id': 'light.bathroom'}, 'fields': {'title': 'Lights', 'title2': '', 'icon': '', 'units': '%', 'level': '', 'state_text': '', 'icon_style': ''}, 'icons': {'icon_on': 'mdi-lightbulb-on', 'icon_off': 'mdi-lightbulb-outline'}, 'static_icons': {'icon_up': 'fas-plus', 'icon_down': 'fas-minus'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'level_style': 'color: #fff;', 'unit_style': 'color: #fff;', 'level_up_style': 'color: #888;', 'level_down_style': 'color: #888;', 'widget_style': 'background-color: #444;'}, 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'icon_off': 'mdi-lightbulb-outline', 'icon_on': 'mdi-lightbulb-on', 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-getting-ready"] = new baseswitch("default-getting-ready", "", "default", {'widget_type': 'baseswitch', 'entity': 'script.getting_ready', 'state_inactive': 'off', 'state_active': 'on', 'enable': 1, 'momentary': 1000, 'ignore_state': 1, 'post_service_active': {'service': 'homeassistant/turn_on', 'entity_id': 'script.getting_ready'}, 'post_service_inactive': {'service': 'homeassistant/turn_off', 'entity_id': 'script.getting_ready'}, 'fields': {'title': 'Getting Ready', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'fas-th-large', 'icon_off': 'fas-th-large'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-fluxer"] = new baseswitch("default-fluxer", "", "default", {'widget_type': 'baseswitch', 'entity': 'switch.bathroom_fluxer', 'state_active': 'on', 'state_inactive': 'off', 'enable': 1, 'post_service_active': {'service': 'homeassistant/turn_on', 'entity_id': 'switch.bathroom_fluxer'}, 'post_service_inactive': {'service': 'homeassistant/turn_off', 'entity_id': 'switch.bathroom_fluxer'}, 'fields': {'title': 'Fluxer', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'fas-circle', 'icon_off': 'far-circle'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-speaker"] = new basemedia("default-speaker", "", "default", {'widget_type': 'basemedia', 'entity': 'media_player.cast_bathroom_speaker', 'post_service_next': {'service': 'media_player/media_next_track', 'entity_id': 'media_player.cast_bathroom_speaker'}, 'post_service_previous': {'service': 'media_player/media_previous_track', 'entity_id': 'media_player.cast_bathroom_speaker'}, 'post_service_play_pause': {'service': 'media_player/media_play_pause', 'entity_id': 'media_player.cast_bathroom_speaker'}, 'post_service_pause': {'service': 'media_player/media_pause', 'entity_id': 'media_player.cast_bathroom_speaker'}, 'post_service_stop': {'service': 'media_player/media_stop', 'entity_id': 'media_player.cast_bathroom_speaker'}, 'post_service_level': {'service': 'media_player/volume_set', 'entity_id': 'media_player.cast_bathroom_speaker'}, 'fields': {'title': 'Speaker', 'artist': '', 'media_title': '', 'album': '', 'play_icon_style': '', 'pause_icon_style': '', 'previous_icon_style': '', 'next_icon_style': '', 'state_text': '', 'level': ''}, 'icons': {'play_icon': 'fas-play', 'pause_icon': 'fas-pause'}, 'static_icons': {'previous_icon': 'fas-step-backward', 'next_icon': 'fas-step-forward', 'icon_up': 'fas-plus', 'icon_down': 'fas-minus'}, 'static_css': {'previous_icon_style': 'color: #888;', 'next_icon_style': 'color: #888;', 'title_style': 'color: #fff;', 'artist_style': 'color: #fff;', 'album_style': 'color: #fff;', 'media_title_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'level_style': 'color: #fff;', 'level_up_style': 'color: #888;', 'level_down_style': 'color: #888;', 'widget_style': 'background-color: #444;', 'units_style': 'color: #fff;'}, 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'icon_on': 'mdi-speaker-wireless', 'icon_off': 'mdi-speaker-wireless', 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-fan"] = new baseswitch("default-fan", "", "default", {'widget_type': 'baseswitch', 'entity': 'switch.bathroom_fan_switch', 'state_active': 'on', 'state_inactive': 'off', 'enable': 1, 'post_service_active': {'service': 'homeassistant/turn_on', 'entity_id': 'switch.bathroom_fan_switch'}, 'post_service_inactive': {'service': 'homeassistant/turn_off', 'entity_id': 'switch.bathroom_fan_switch'}, 'fields': {'title': 'Fan', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'fas-circle', 'icon_off': 'far-circle'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-wake-up"] = new baseswitch("default-wake-up", "", "default", {'widget_type': 'baseswitch', 'entity': 'script.bathroom_wake_up', 'state_active': 'on', 'state_inactive': 'off', 'enable': 1, 'post_service_active': {'service': 'homeassistant/turn_on', 'entity_id': 'script.bathroom_wake_up'}, 'post_service_inactive': {'service': 'homeassistant/turn_off', 'entity_id': 'script.bathroom_wake_up'}, 'fields': {'title': 'Wake-Up', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'mdi-sleep-off', 'icon_off': 'mdi-sleep'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'use_hass_icon': 0, 'icon_off': 'mdi-sleep', 'icon_on': 'mdi-sleep-off', 'namespace': 'default'})
    
        widgets["default-motion"] = new baseswitch("default-motion", "", "default", {'widget_type': 'baseswitch', 'entity': 'switch.bathroom_motion', 'state_active': 'on', 'state_inactive': 'off', 'enable': 1, 'post_service_active': {'service': 'homeassistant/turn_on', 'entity_id': 'switch.bathroom_motion'}, 'post_service_inactive': {'service': 'homeassistant/turn_off', 'entity_id': 'switch.bathroom_motion'}, 'fields': {'title': 'Motion', 'title2': '', 'icon': '', 'icon_style': '', 'state_text': ''}, 'icons': {'icon_on': 'fas-circle', 'icon_off': 'far-circle'}, 'static_icons': [], 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-temperature"] = new basedisplay("default-temperature", "", "default", {'widget_type': 'basedisplay', 'entity': 'sensor.bathroom_temperature', 'entity_to_sub_entity_attribute': '', 'sub_entity': '', 'sub_entity_to_entity_attribute': '', 'fields': {'title': 'Temperature', 'title2': '', 'value': '', 'unit': '', 'state_text': ''}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;font-size: 100%;', 'widget_style': 'background-color: #444;', 'container_style': ''}, 'css': {'value_style': 'color: #00aaff;font-size: 250%;', 'text_style': 'color: #fff;font-size: 100%;', 'unit_style': 'color: #00aaff;font-size: 100%;'}, 'icons': [], 'static_icons': [], 'use_hass_icon': 1, 'namespace': 'default'})
    
        widgets["default-humidity"] = new basedisplay("default-humidity", "", "default", {'widget_type': 'basedisplay', 'entity': 'sensor.bathroom_relative_humidity', 'entity_to_sub_entity_attribute': '', 'sub_entity': '', 'sub_entity_to_entity_attribute': '', 'fields': {'title': 'Humidity', 'title2': '', 'value': '', 'unit': '', 'state_text': ''}, 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'state_text_style': 'color: #fff;font-size: 100%;', 'widget_style': 'background-color: #444;', 'container_style': ''}, 'css': {'value_style': 'color: #00aaff;font-size: 250%;', 'text_style': 'color: #fff;font-size: 100%;', 'unit_style': 'color: #00aaff;font-size: 100%;'}, 'icons': [], 'static_icons': [], 'use_hass_icon': 1, 'namespace': 'default'})
    

    // Setup click handler to cancel timeout navigations

    $( ".gridster" ).click(function(){
        clearTimeout(myTimeout);
        if (myTimeoutSticky) {
            myTimeout = setTimeout(function() { navigate(myTimeoutUrl); }, myTimeoutDelay);
        }
    });

    // Set up timeout

    var myTimeout;
    var myTimeoutUrl;
    var myTimeoutDelay;
    var myTimeoutSticky = 0;

    if (location.search != "")
    {
        var query = location.search.substr(1);
        var result = {};
        query.split("&").forEach(function(part) {
        var item = part.split("=");
        result[item[0]] = decodeURIComponent(item[1]);
        });

        if ("timeout" in result && "return" in result)
        {
            url = result.return
            argcount = 0
            for (arg in result)
            {
                if (arg != "timeout" && arg != "return" && arg != "sticky")
                {
                    if (argcount == 0)
                    {
                        url += "?";
                    }
                    else
                    {
                        url += "?";
                    }
                    argcount ++;
                    url += arg + "=" + result[arg]
                }
            }
            if ("sticky" in result)
            {
                myTimeoutSticky = (result.sticky == "1");
            }
            myTimeoutUrl = url;
            myTimeoutDelay = result.timeout * 1000;
            myTimeout = setTimeout(function() { navigate(url); }, result.timeout * 1000);
        }
    }

    // Start listening for HA Events
    if (location.protocol == 'https:')
    {
        wsprot = "wss:"
    }
    else
    {
        wsprot = "ws:"
    }
    var stream_url = wsprot + '//' + location.host + '/stream'
    ha_status(stream_url, "Bathroom", widgets);

});