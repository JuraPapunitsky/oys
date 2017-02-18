/*
 * jQuery x-Tools v1.2.0
 *
 * Copyright 2013, Vladimir Volkov.
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Requires: jQuery JavaScript Library
 * http://jquery.com/
 */



/* Init Events ****************************************************************/
(function($) {
    'use strict';

    $(function() {
        $('html').addClass('dom-ready').removeClass('no-js');
    });

    $(window).load(function() {
        $('html').addClass('win-load');
    });
}(jQuery));
/* End Init Events ************************************************************/



/* Browser Identification *****************************************************/
(function($) {
    'use strict';

    function XBList() {
        this.aList = [];
    }

    XBList.prototype = {

        _2Condition: function(c) {
            return c === undefined ? {} : ($.isPlainObject(c) ? c : { userAgent: c });
        },

        add: function(name, allow, deny) {
            this.aList.push({
                name: name,
                oAllow: this._2Condition(allow),
                oDeny: this._2Condition(deny)
            });
            return this;
        },

        get: function() {
            var i, j, state;
            for (i = 0; i< this.aList.length; i++) {
                state = true;
                for (j in this.aList[i].oAllow) {
                    if (!this.aList[i].oAllow[j].test(navigator[j])) {
                        state = false;
                        break;
                    }
                }
                for (j in this.aList[i].oDeny) {
                    if (this.aList[i].oDeny[j].test(navigator[j])) {
                        state = false;
                        break;
                    }
                }
                if (state) {
                    return this.aList[i].name;
                }
            }
            return null;
        }
    };

    var oName = new XBList(),
        oOS = new XBList(),
        oPlatform = new XBList(),
        oEngine = new XBList(),
        getVersion = function() {
            return (/.+(Chrome|Firefox|Version|OPR|MSIE)(\/| )([0-9\.]+)/).exec(navigator.userAgent)[3] || null;
        },
        fnUpdate = function() {
            $.xBrowser = {
                name: oName.get(),
                os: oOS.get(),
                platform: oPlatform.get(),
                engine: oEngine.get(),
                version: getVersion()
            };
            $('html')
                .removeClass('chrome firefox safari opera ie android ios win mac linux mobile desktop webkit gecko presto trident')
                .addClass($.xBrowser.os + ' ' + $.xBrowser.platform + ' ' + $.xBrowser.engine + ' ' + $.xBrowser.name + ' ' + $.xBrowser.name + parseInt($.xBrowser.version, 10));
        };

    oName .add('chrome', { userAgent: /Chrome/, vendor: /Google/ })
        .add('firefox', /Firefox/)
        .add('safari', { userAgent: /Safari/, vendor: /Apple/ })
        .add('opera', /Opera/)
        .add('opera', { vendor: /Opera/})
        .add('ie', /MSIE/);

    oOS .add('android', /Android/) .add('ios', /iPad|iPhone|iPod/) .add('win', /Windows/) .add('mac', /Macintosh/) .add('linux', /Linux/);
    oPlatform .add('mobile', /Android|iPad|iPhone|iPod/) .add('desktop', /Windows|Macintosh|Linux/);
    oEngine .add('webkit', /WebKit/) .add('gecko', /Gecko/, /WebKit/) .add('presto', /Presto/) .add('trident', /Trident|MSIE (7|6|5)/);

    fnUpdate();
}(jQuery));
/* End Browser Identification *************************************************/



/* IE lte 8 HTML5 support *****************************************************/
(function($) {
    'use strict';

    if ($.xBrowser.name === 'ie' && $.xBrowser.version < 9) {
        var tags = [
            'article',
            'aside',
            'figcaption',
            'figure',
            'footer',
            'header',
            'hgroup',
            'mark',
            'nav',
            'section',
            'time'
        ];
        for (var i = 0; i < tags.length; i++) {
            document.createElement(tags[i]);
        }
    }
}(jQuery));
/* End IE lte 8 HTML5 support *************************************************/



/* Log ************************************************************************/
(function($) {
    'use strict';

    $.xLog = function(obj, deep) {
        try {
            window.console.log.apply(window.console, $.merge([time() + ' |'], arguments));
        } catch(e) {}
    };

    var time = function() {
            var d = new Date();
            return add0(d.getHours(), 2) + ':' + add0(d.getMinutes(), 2) + ':' + add0(d.getSeconds(), 2) + ':' + add0(d.getMilliseconds(), 3, true);
        },

        add0 = function(num, r, after) {
            num = num.toString();
            while (num.length < r) {
                if (after) {
                    num += '0';
                } else {
                    num = '0' + num;
                }
            }
            return num;
        };
}(jQuery));
/* End Log ********************************************************************/



/* Events *********************************************************************/
(function($) {
    'use strict';

    $.xEvent = {
        bind: function(name, cb) {
            get(name).add(cb);
        },

        unbind: function(name, cb) {
            get(name).remove(cb);
        },

        trigger: function(name) {
            get(name).fire(Array.prototype.slice.call(arguments, 1));
        }
    };

    var list = {},
        get = function(name) {
            if (list[name] === undefined) {
                list[name] = $.Callbacks('unique');
            }
            return list[name];
        };
}(jQuery));
/* End Events *****************************************************************/



/* jQuery Functions ***********************************************************/
(function($) {
    'use strict';

    $.fn.xIndex = function(el) {
        return ((this.index(el) + 1) || 1) - 1;
    };
}(jQuery));
/* End jQuery Functions *******************************************************/



/* Math ***********************************************************************/
(function($) {
    'use strict';

    var round = function(num, order, fn) {
        var cAll = num.toString().replace('.', '').length,
            cInt = Math.floor(num).toString().length,
            k;
        order = (cAll + order) % cAll;
        k = Number('1e' + (cInt - order));
        return fn(num / k) * k;
    };

    $.xMath = {
        floor: function(num, order) {
            return round(num, order, Math.floor);
        },

        round: function(num, order) {
            return round(num, order, Math.round);
        },

        ceil: function(num, order) {
            return round(num, order, Math.ceil);
        }
    };
}(jQuery));
/* End Math *******************************************************************/



/* Cookies ********************************************************************/
(function($) {
    'use strict';

    $.xCookie = function(name, value, params) {
        if (value === undefined) {
            return get()[name];
        } else {
            var obj = {};
            obj[name] = value;
            set($.extend(obj, params));
            return true;
        }
    };

    $.xRemoveCookie = function(name, params) {
        var obj = {
            expires: new Date()
        };
        obj[name] = '';

        set($.extend(obj, params));
    };

    var get = function() {
            var result = {};

            $.each(document.cookie.split('; '), function() {
                var cookie = this.split('=');
                result[cookie[0]] = cookie[1];
            });

            return result;
        },

        set = function(params) {
            if (params.expires !== undefined) {
                params.expires = ($.type(params.expires) === 'number' ? (new Date((new Date()).getTime() + params.expires * 1000 * 60 * 60 * 24)) : params.expires).toUTCString();
            }
            document.cookie = $.map(params, function(el, index) {
                return index + '=' + el;
            }).join(';');
        };
}(jQuery));
/* End Cookies ****************************************************************/



/* Hash ***********************************************************************/
(function($) {
    'use strict';

    $.xHash = function(hash, replace) {
        if (hash === undefined) {
            return get();
        } else {
            if (replace) {
                return replaceHash(hash);
            } else {
                return set(hash);
            }
        }
    };

    var get = function() {
            return decodeURIComponent(window.location.hash.substr(1));
        },

        set = function(hash) {
            var h = '#' + encodeURIComponent(hash);
            window.location.hash = h;
            return h;
        },

        replaceHash = function(hash) {
            var h = '#' + encodeURIComponent(hash);
            var wl = window.location;
            wl.replace(wl.protocol + '//' + wl.hostname + wl.pathname + wl.search + h);
            return h;
        };
}(jQuery));
/* End Hash *******************************************************************/



/* Preload ********************************************************************/
(function($) {
    'use strict';

    $.fn.xPreload = function(cb) {
        return preload($.map(this.filter('img').add(this.find('img')).toArray(), function() {
            return $(this).attr('src');
        }), cb, this);
    };

    $.xPreload = function(src, cb) {
        return preload($.isArray(src) ? src : [src], cb, src);
    };

    var preload = (function() {
        var items = 0,

            fnCreate = function() {
                return items++ === 0 ? $('<div id="x-preload" style="display: none;"></div>').appendTo('body') : $('#x-preload');
            },

            fnDestroy = function() {
                if (--items === 0) {
                    $('#x-preload').remove();
                }
            },

            fnLoad = (function() {
                var re = /^.+\.(jpg|jpeg|png|gif)$/;
                return function(src) {
                    if (re.test(src)) {
                        var dComplete = $.Deferred();
                        $('<img>').load(function() {
                            $(this).detach();
                            fnDestroy();
                            dComplete.resolve();
                        }).attr('src', src).appendTo(fnCreate());
                        return dComplete;
                    } else {
                        return $.get(src);
                    }
                };
            }());


        return function(array, cb, arg) {
            var dComplete = $.Deferred(),
                dArray = [];

            for (var i = 0; i < array.length; i++) {
                dArray.push(fnLoad(array[i]));
            }
            $.when.apply(null, dArray).done(function() {
                dComplete.resolve(arg);
            });

            return dComplete;
        };
    }());
}(jQuery));
/* End Preload ****************************************************************/



/* Style **********************************************************************/
(function($) {
    'use strict';

    $.fn.xStyle = function(params) {
        params = $.extend(true, {
            preload: [],
            clazz: {
                wrap:        'x-style-wrap',
                title:       'e-title',
                holder:      'e-holder',
                placeholder: 'e-placeholder',
                empty:       'is-empty',
                focus:       'is-focus',
                hover:       'is-hover',
                active:      'is-active',
                mobile:      'm-mobile'
            },
            text:       '<div class="x-text">#element#<i class="bg"></i></div>',
            password:   '<div class="x-password">#element#<i class="bg"></i></div>',
            textarea:   '<div class="x-textarea">#element#<i class="bg"></i></div>',
            checkbox:   '<a class="x-checkbox" href="javascript:void(0)">#element#<i class="bg"></i></a>',
            radio:      '<a class="x-radio" href="javascript:void(0)">#element#<i class="bg"></i></a>',
            button:     '<div class="x-button">#element#<span class="e-title"></span><i class="bg"></i></div>',
            select:     '<div class="x-select">#element#<span class="e-title"></span><i class="bg"></i><i class="e-icon"></i></div>',
            selectDrop: '<div class="x-select-drop"><ul class="r-list">#list#</ul><i class="bg"></i></div>',
            selectItem: '<li><a>#title#</a></li>',
            file:       '<div class="x-file"><div class="e-holder">#element#</div><span class="e-title"></span></div>',
            fileFormat: 'File: $name.$ext'
        }, params);

        var $el = $($.grep(this.toArray(), function(el) {
                return fnGetType($(el)) && $(el).data('x-style-complete') === undefined;
            })),
            $result = $([]);

        $result
            .add(fnStyleText($el, params))
            .add(fnStylePassword($el, params))
            .add(fnStyleTextarea($el, params))
            .add(fnStyleCheckbox($el, params))
            .add(fnStyleRadio($el, params))
            .add(fnStyleButton($el, params))
            .add(fnStyleSelect($el, params))
            .add(fnStyleFile($el, params));

        $el.add($result.addClass(params.clazz.wrap)).data('x-style-complete', true);
        $.xPreload(params.preload);
        return $result;
    };

    var fnGetType = function($el) {
            if ($el.is('input[type="text"], input[type="password"], input[type="checkbox"], input[type="radio"], input[type="file"]')) {
                return $el.attr('type');
            } else if ($el.is('a, button, input[type="button"], input[type="submit"], input[type="reset"]')) {
                return 'button';
            } else if ($el.is('textarea')) {
                return 'textarea';
            } else if ($el.is('select')) {
                return 'select';
            }
            return null;
        },

        fnReset = function($el, handler) {
            $el.closest('form').on('reset', function() {
                setTimeout(handler, 25);
            });
        },

        fnCreate = function($el, type, params) {
            var template = params[type].replace('#element#', '<span class="x-style-temp-el"></span>'),
                $wrap = $(template).insertAfter($el).addClass($el.attr('class') || '');

            $wrap.find('.x-style-temp-el').replaceWith($el.detach());
            fnPlaceholder($wrap, $el, type, params);

            return $wrap;
        },

        fnPlaceholder = function($wrap, $el, type, params) {
            if ($.inArray(type, ['text', 'password', 'textarea']) === -1 || $el.attr('placeholder') === undefined) { return; }

            var fnShow = function() {
                    if ($el.val() === '') {
                        $wrap.addClass(params.clazz.empty);
                        $ph.show();
                    }
                },

                fnHide = function() {
                    $wrap.removeClass(params.clazz.empty);
                    $ph.hide();
                },

                text = $el.attr('placeholder'),
                $ph;

            $el.removeAttr('placeholder');
            $ph = $('<span class="' + params.clazz.placeholder + '">' + text + '</span>').css({display: 'none'}).insertAfter($el);
            fnShow();

            $el.focus(fnHide).blur(fnShow);
            fnReset($el, function() {
                fnShow();
            });
        },

        fnHover = function($el, $w, params) {
            $el.on('mouseenter', function() {
                $w.addClass(params.clazz.hover);
            }).on('mouseleave', function() {
                $w.removeClass(params.clazz.hover);
            });
        },

        fnFocus = function($el, $w, params) {
            $el.focus(function() {
                $w.addClass(params.clazz.focus);
            }).blur(function() {
                $w.removeClass(params.clazz.focus);
            });
        },

        fnStyleText = function($list, params) {
            return $list.filter('input[type="text"]').map(function() {
                var $el = $(this),
                    $w = fnCreate($el, 'text', params);
                fnHover($w, $w, params);
                fnFocus($el, $w, params);
                return $w[0];
            });
        },

        fnStylePassword = function($list, params) {
            return $list.filter('input[type="password"]').map(function() {
                var $el = $(this),
                    $w = fnCreate($el, 'password', params);
                fnHover($w, $w, params);
                fnFocus($el, $w, params);
                return $w[0];
            });
        },

        fnStyleTextarea = function($list, params) {
            return $list.filter('textarea').map(function() {
                var $el = $(this),
                    $w = fnCreate($el, 'textarea', params);
                fnHover($w, $w, params);
                fnFocus($el, $w, params);
                return $w[0];
            });
        },

        fnStyleCheckbox = function($list, params) {
            return $list.filter('input[type="checkbox"]').map(function() {
                var $el = $(this),
                    $w = fnCreate($el, 'checkbox', params),

                    hChange = function() {
                        $w.toggleClass(params.clazz.active, $el[0].checked);
                    },

                    hClick = function(ev) {
                        if ($el.attr('disabled')) { return; }
                        if (ev === undefined || ev.target !== $el[0]) {
                            $el[0].checked = !$el[0].checked;
                            $el.trigger('change');
                        }
                    },

                    fnBindFocus = function() {
                        fnFocus($w, $w, params);
                        $w.on('click', function() {
                            if ($el.attr('disabled')) { return; }
                            $w.trigger('focus');
                        }).on('keydown', function(ev) {
                            if (ev.keyCode === 32) {
                                hClick();
                                ev.preventDefault();
                            }
                        });
                    };

                hChange();
                $el.on('change', hChange);

                $w.on('click', hClick).on('mousedown', function(e) {
                    e.preventDefault();
                });

                fnHover($w, $w, params);
                fnBindFocus();
                fnReset($el, hChange);

                return $w[0];
            });
        },

        fnStyleRadio = function($list, params) {
            return $list.filter('input[type="radio"]').map(function() {
                var $el = $(this),
                    $w = fnCreate($el, 'radio', params),
                    $group = $('input[type="radio"][name="' + $el.attr('name') + '"]'),

                    hChange = function() {
                        $w.toggleClass(params.clazz.active, $el[0].checked);
                    },

                    hClick = function(ev) {
                        if ($el.attr('disabled')) { return; }
                        if (ev === undefined || ev.target !== $el[0] && !$el[0].checked) {
                            $el[0].checked = true;
                            $group.trigger('change');
                        } else if (ev.target === $el[0]) {
                            $group.trigger('change');
                        }
                    },

                    fnBindFocus = function() {
                        fnFocus($w, $w, params);
                        $w.on('click', function() {
                            if ($el.attr('disabled')) { return; }
                            $w.trigger('focus');
                        }).on('keydown', function(ev) {
                            if (ev.keyCode === 32) {
                                hClick();
                                ev.preventDefault();
                            }
                        });
                    };

                hChange();
                $el.change(hChange);

                $w.on('click', hClick).on('mousedown', function(e) {
                    e.preventDefault();
                });

                fnHover($w, $w, params);
                fnBindFocus();
                fnReset($el, hChange);

                return $w[0];
            });
        },

        fnStyleButton = function($list, params) {
            return $list.filter('a, button, input[type="button"], input[type="submit"], input[type="reset"]').map(function() {
                var $el = $(this),
                    $w = fnCreate($el, 'button', params),
                    isInput = !$el.is('a, button'),

                    fnBindFocus = function() {
                        fnFocus($el, $w, params);
                        $w.on('click', function() {
                            $el.on('focus');
                        });
                    };

                $w.find('.' + params.clazz.title).html(isInput ? ($el.val() || '') : $el.html());
                fnHover($w, $w, params);
                fnBindFocus();

                return $w[0];
            });
        },

        fnStyleSelect = function($list, params) {
            return $list.filter('select').map(function() {
                var $el = $(this),
                    $oList = $el.find('option'),
                    $w = fnCreate($el, 'select', params),
                    $t = $w.find('.' + params.clazz.title),
                    mobile = $.xBrowser.platform === 'mobile',

                    $liList = $oList.map(function() {
                        return $(params.selectItem.replace('#title#', $(this).html()))[0];
                    }),

                    $dw = (function() {
                        var $w = $(params.selectDrop.replace('#list#', '<span class="x-style-temp-el"></span>')).addClass($el.attr('class') || '');
                        $w.find('.x-style-temp-el').replaceWith($liList);
                        return $w;
                    }()),

                    fnUpdate = function() {
                        var index = $el[0].selectedIndex;
                        $t.html($oList.eq(index).html());
                        $liList.removeClass(params.clazz.active).eq(index).addClass(params.clazz.active);
                    },

                    fnShow = function() {
                        if ($el.attr('disabled')) { return; }

                        $w.off('click', fnShow);
                        fnPosition();
                        $dw.appendTo('body');
                        $w.addClass(params.clazz.active).on('click', fnHide);

                        $('body').on('click', hBodyClick);
                        $(window).on({
                            resize: fnPosition,
                            scroll: fnPosition
                        });
                    },

                    fnHide = function() {
                        $(window).off({
                            resize: fnPosition,
                            scroll: fnPosition
                        });
                        $('body').off('click', hBodyClick);
                        $w.removeClass(params.clazz.active).off('click', fnHide);
                        $dw.detach();
                        $w.on('click', fnShow);
                    },

                    hBodyClick = function(e) {
                        if ($dw[0] !== e.target && !$dw.find(e.target).length && $w[0] !== e.target && !$w.find(e.target).length) {
                            fnHide();
                        }
                    },

                    hItemClick = function(e) {
                        var index = $liList.index(this);
                        if ($el[0].selectedIndex !== index) {
                            $el[0].selectedIndex = index;
                            $el.change();
                        }
                        fnHide();
                        $el.focus();
                    },

                    fnPosition = function() {
                        $dw.css({
                            top: $w.offset().top,
                            left: $w.offset().left,
                            width: $w.outerWidth()
                        });
                    },

                    fnBindFocus = function() {
                        fnFocus($el, $w, params);
                        $w.click(function() {
                            if ($el.attr('disabled')) { return; }
                            $el.focus();
                        });
                    };

                fnUpdate();
                $el.change(fnUpdate);

                if (!mobile) {
                    $liList.click(hItemClick);
                    $w.on('click', fnShow).mousedown(function(e) {
                        e.preventDefault();
                    });
                    fnHover($w, $w, params);
                    fnBindFocus();
                } else {
                    $w.addClass(params.clazz.mobile);
                }

                fnReset($el, fnUpdate);
            });
        },

        fnStyleFile = function($list, params) {
            return $list.filter('input[type="file"]').map(function() {
                var $el = $(this),
                    $w = fnCreate($el, 'file', params),
                    $h = $w.find('.' + params.clazz.holder),
                    ph = $el.attr('placeholder') || '',
                    $t = $w.find('.' + params.clazz.title),

                    fnUpdate = function() {
                        var str = $el.val().replace(/^.+?[\/\\]([^\/\\]+?)(?:\.([^\/\\]+))?$/, params.fileFormat.replace('$name', '$1').replace('$ext', '$2'));
                        $t.html(str !== '' ? str : ph);
                        $w.toggleClass(params.clazz.active, str !== '');
                    },

                    fnBindFocus = function() {
                        fnFocus($el, $w, params);
                        $h.on('click', function() {
                            $el.trigger('focus');
                        });
                    };

                $el.removeAttr('placeholder');
                fnUpdate();

                $el.on('change', fnUpdate);
                fnHover($h, $w, params);
                fnBindFocus();
                fnReset($el, fnUpdate);
            });
        };
}(jQuery));
/* End Style ******************************************************************/



/* Ajax Replace / Append / Prepend ********************************************/
(function($) {
    'use strict';

    $.fn.xAjaxReplace = function(params) {
        return fnAjax(this, 'replace', params);
    };

    $.fn.xAjaxAppend = function(params) {
        return fnAjax(this, 'append', params);
    };

    $.fn.xAjaxPrepend = function(params) {
        return fnAjax(this, 'prepend', params);
    };


    var fnAjax = (function() {
        var oDataSet = {
                a: {
                    event: 'click',
                    url:   'href',
                    data:  'undefined'
                },
                form: {
                    event: 'submit',
                    url:   'action',
                    data:  '$el.serialize()'
                }
            },
            oActionSet = {
                replace: '$(id).after($html).remove()',
                append:  '$(id).append($html)',
                prepend: '$(id).prepend($html)'
            };

        return function($el, action, params) {
            params = $.extend({
                target: 'js-target',
                cbAfter: $.noop
            }, params);

            return $el.each(function() {
                var $el = $(this),
                    oData = oDataSet[$el[0].tagName.toLowerCase()];

                if (oData === undefined) { return; }

                var fnRequest = (function() {
                    var url = $el.attr(oData.url),
                        id = $el.attr(params.target);

                    return function(ev) {
                        $.ajax({
                            url: url,
                            data: eval(oData.data),
                            success: function(html) {
                                var $html = $(html);
                                eval(oActionSet[action]);
                                params.cbAfter($html);
                            }
                        });
                        ev.preventDefault();
                    };
                }());

                $el.on(oData.event, fnRequest);
            });
        };
    }());
}(jQuery));
/* End Ajax Replace / Append / Prepend ****************************************/