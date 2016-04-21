// browser test
if (!'classList' in document.createElement('a')) {
    document.write('<p class="browser-message">Sorry to have to bring this up, but your browser is outdated. Some site features might be broken. Please update or try <a href="https://www.getfirefox.com">Firefox</a> or <a href="https://www.google.com/chrome/">Chrome</a></p>');
    throw new Error('Outdated browser. Stopping');
}


var WHISKIES = (function (window, document) {

    'use strict';


    ////////////////////////
    //  helper functions  //
    ////////////////////////

    // fast forEach
    function forEach(collection, fn) {
        if (!collection) {
            return false;
        }
        var i = 0,
            limit = collection.length;
        for (; i < limit; i++) {
            fn(collection[i], i);
        }
    }
    function forEachReversed(collection, fn) {
        if (!collection) {
            return false;
        }
        var i = collection.length - 1;
        for (; i >= 0; i--) {
            fn(collection[i], i);
        }
    }

    // array conversion, faster than [].slice.call()
    function toArray(collection) {
        var result = [];
        forEach(collection, function (item) {
            result.push(item);
        });
        return result;
    }

    // parent traversal helpers
    function getParents(el) {
        var result = [];
        while (el !== document.documentElement) {
            result.push(el);
            el = el.parentNode;
        }
        return result;
    }
    function getParentsByTagName(el, tag) {
        tag = tag.toLowerCase();
        return getParents(el).filter(function (candidate) {
            return !!candidate.tagName && candidate.tagName.toLowerCase() === tag;
        });
    }
    function getParentsByClassName(el, cl) {
        return getParents(el).filter(function (candidate) {
            return !!candidate.className && candidate.classList.contains(cl);
        });
    }

    // get a timestamp
    function now() {
        'use strict';
        return Date.now || new Date().getTime();
    }

    // throttle and debounce from underscore.js
    function throttle(func, wait, options) {
        'use strict';
        var context, args, result,
            timeout = null,
            previous = 0;
        if (!options) {
            options = {};
        }
        var later = function () {
            previous = options.leading === false ? 0 : now();
            timeout = null;
            result = func.apply(context, args);
            if (!timeout) {
                context = args = null;
            }
        };
        return function () {
            var now = now();
            if (!previous && options.leading === false) {
                previous = now;
            }
            var remaining = wait - (now - previous);
            context = this;
            args = arguments;
            if (remaining <= 0 || remaining > wait) {
                clearTimeout(timeout);
                timeout = null;
                previous = now;
                result = func.apply(context, args);
                if (!timeout) {
                    context = args = null;
                }
            } else if (!timeout && options.trailing !== false) {
                timeout = setTimeout(later, remaining);
            }
            return result;
        };
    }
    function debounce(func, wait, immediate) {
        'use strict';
        var timeout, args, context, timestamp, result;
        var later = function () {
            var last = now() - timestamp;
            if (last < wait && last > 0) {
                timeout = setTimeout(later, wait - last);
            } else {
                timeout = null;
                if (!immediate) {
                    result = func.apply(context, args);
                    if (!timeout) {
                        context = args = null;
                    }
                }
            }
        };
        return function () {
            context = this;
            args = arguments;
            timestamp = now();
            var callNow = immediate && !timeout;
            if (!timeout) {
                timeout = setTimeout(later, wait);
            }
            if (callNow) {
                result = func.apply(context, args);
                context = args = null;
            }
            return result;
        };
    };



    ///////////////////////
    //  generic toggles  //
    ///////////////////////

    // <el data-toggle-target="[keyword|selector]" />

    var toggles = (function () {
        // use this module on .toggle elements by default
        var initEls = document.querySelectorAll('[data-toggle-target]'),
            toggleList = [],
            activeClass = 'is-active';

        // individual toggle object; stores element and targets
        function Toggle(el) {
            var that = this;
            this.origin = el;
            this.targets = findTargets(el);
            el.addEventListener('click', function (ev) {
                ev.preventDefault();
                that.activate();
            });
        }

        // parses a target string and returns a matching array
        function findTargets(el) {
            var targetString = el.getAttribute('data-toggle-target');
            if (!targetString) {
                return [];
            } else if (targetString === 'next') {
                return [el.nextElementSibling];
            } else if (targetString === 'prev') {
                return [el.previousElementSibling];
            } else if (targetString === 'parent') {
                return [el.parentNode];
            } else if (targetString === 'parentnext') {
                return [el.parentNode.nextElementSibling];
            } else if (targetString === 'parentparentnext') {
                return [el.parentNode.parentNode.nextElementSibling];
            }
            return toArray(document.querySelectorAll(targetString));
        }

        // make toggle go
        Toggle.prototype.activate = function (force) {
            forEach([this.origin].concat(this.targets), function (el) {
                if (typeof force === 'boolean') {
                    el.classList.toggle(activeClass, force);
                } else {
                    el.classList.toggle(activeClass);
                }
            });
        };

        // public: make node or nodeList toggleable
        function add(els) {
            forEach(els, function (el) {
                toggleList.push(new Toggle(el));
            });
        }

        // public: returns an array of all toggles on the page
        function list() {
            return toggleList;
        }

        // public: initialize by adding default elements
        function init() {
            add(initEls);
        }

        return {
            add: add,
            list: list,
            init: init
        };
    }());


    //////////////////
    //  Miscellany  //
    //////////////////

    function addParallax() {
        var parallaxEl = document.querySelector('.article-image__positioner'),
            parallaxScale = 10,
            pageHeight = 0,
            effectiveHeight = 0,
            currentTransform = 0;

        function updatePageHeight() {
            pageHeight = document.body.clientHeight;
            effectiveHeight = pageHeight - window.innerHeight;
        }

        function drawParallax() {
            parallaxEl.style.webkitTransform = 'translateY(' + currentTransform + 'px)';
            parallaxEl.style.transform = 'translateY(' + currentTransform + 'px)';
        }

        function updateParallax() {
            var percentageScrolled = (window.pageYOffset / effectiveHeight) * 2 - 1;
            currentTransform = parallaxScale * percentageScrolled * -1;
            window.requestAnimationFrame(drawParallax);
        }

        updatePageHeight();

        if (parallaxEl && effectiveHeight > 0) {
            parallaxEl.style.top = (parallaxScale * -1) + 'px';
            parallaxEl.style.bottom = (parallaxScale * -1) + 'px';
            updateParallax();
            document.addEventListener('scroll', updateParallax);
            document.addEventListener('resize', updatePageHeight);
        }
    }


    function colorizePostList(postList) {
        var items = toArray(postList.children),
            startColor = [11, 108, 115],  // #0b6c73
            endColor = [39, 103, 52],  // #276734
            rStep = (endColor[0] - startColor[0]) / items.length,
            gStep = (endColor[1] - startColor[1]) / items.length,
            bStep = (endColor[2] - startColor[2]) / items.length;

        forEach(items, function (item, index) {
            item.children[0].style.backgroundColor = 'rgb(' +
                Math.floor(startColor[0] + rStep * index) + ',' +
                Math.floor(startColor[1] + gStep * index) + ',' +
                Math.floor(startColor[2] + bStep * index) + ')';
        });
    }
    forEach(document.getElementsByClassName('post-list'), colorizePostList);


    //////////////////////
    //  initialization  //
    //////////////////////

    var init = function () {
        if (Modernizr && !Modernizr.touchevents) {
            addParallax();
        }
        toggles.init();
        document.documentElement.classList.remove('no-js');
        document.documentElement.classList.add('js');
    };


    //////////////
    //  public  //
    //////////////

    return {
        toggles: toggles,
        init: init
    };

}(window, document));

WHISKIES.init();
