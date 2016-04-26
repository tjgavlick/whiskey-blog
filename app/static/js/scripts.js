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


    // debounce function from lodash with dependency functions
    function isObject(value) {
        var type = typeof value;
        return !!value && (type == 'object' || type == 'function');
    }
    function toNumber(value) {
        if (typeof value == 'number') {
            return value;
        }
        if (isSymbol(value)) {
            return NAN;
        }
        if (isObject(value)) {
            var other = isFunction(value.valueOf) ? value.valueOf() : value;
            value = isObject(other) ? (other + '') : other;
        }
        if (typeof value != 'string') {
            return value === 0 ? value : +value;
        }
        value = value.replace(reTrim, '');
        var isBinary = reIsBinary.test(value);
        return (isBinary || reIsOctal.test(value))
            ? freeParseInt(value.slice(2), isBinary ? 2 : 8)
            : (reIsBadHex.test(value) ? NAN : +value);
    }
    function debounce(func, wait, options) {
        var lastArgs,
            lastThis,
            maxWait,
            result,
            timerId,
            lastCallTime = 0,
            lastInvokeTime = 0,
            leading = false,
            maxing = false,
            trailing = true;

        if (typeof func != 'function') {
            throw new TypeError(FUNC_ERROR_TEXT);
        }
        wait = toNumber(wait) || 0;
        if (isObject(options)) {
            leading = !!options.leading;
            maxing = 'maxWait' in options;
            maxWait = maxing ? nativeMax(toNumber(options.maxWait) || 0, wait) : maxWait;
            trailing = 'trailing' in options ? !!options.trailing : trailing;
        }

        function invokeFunc(time) {
            var args = lastArgs,
                thisArg = lastThis;

            lastArgs = lastThis = undefined;
            lastInvokeTime = time;
            result = func.apply(thisArg, args);
            return result;
        }

        function leadingEdge(time) {
            // Reset any `maxWait` timer.
            lastInvokeTime = time;
            // Start the timer for the trailing edge.
            timerId = setTimeout(timerExpired, wait);
            // Invoke the leading edge.
            return leading ? invokeFunc(time) : result;
        }

        function remainingWait(time) {
            var timeSinceLastCall = time - lastCallTime,
                timeSinceLastInvoke = time - lastInvokeTime,
                result = wait - timeSinceLastCall;

            return maxing ? nativeMin(result, maxWait - timeSinceLastInvoke) : result;
        }

        function shouldInvoke(time) {
            var timeSinceLastCall = time - lastCallTime,
                timeSinceLastInvoke = time - lastInvokeTime;

            // Either this is the first call, activity has stopped and we're at the
            // trailing edge, the system time has gone backwards and we're treating
            // it as the trailing edge, or we've hit the `maxWait` limit.
            return (!lastCallTime || (timeSinceLastCall >= wait) ||
                   (timeSinceLastCall < 0) || (maxing && timeSinceLastInvoke >= maxWait));
        }

        function timerExpired() {
            var time = Date.now();
            if (shouldInvoke(time)) {
                return trailingEdge(time);
            }
            // Restart the timer.
            timerId = setTimeout(timerExpired, remainingWait(time));
        }

        function trailingEdge(time) {
            clearTimeout(timerId);
            timerId = undefined;

            // Only invoke if we have `lastArgs` which means `func` has been
            // debounced at least once.
            if (trailing && lastArgs) {
                return invokeFunc(time);
            }
            lastArgs = lastThis = undefined;
            return result;
        }

        function cancel() {
            if (timerId !== undefined) {
                clearTimeout(timerId);
            }
            lastCallTime = lastInvokeTime = 0;
            lastArgs = lastThis = timerId = undefined;
        }

        function flush() {
            return timerId === undefined ? result : trailingEdge(now());
        }

        function debounced() {
            var time = Date.now(),
                isInvoking = shouldInvoke(time);

            lastArgs = arguments;
            lastThis = this;
            lastCallTime = time;

            if (isInvoking) {
                if (timerId === undefined) {
                    return leadingEdge(lastCallTime);
                }
                if (maxing) {
                    // Handle invocations in a tight loop.
                    clearTimeout(timerId);
                    timerId = setTimeout(timerExpired, wait);
                    return invokeFunc(lastCallTime);
                }
            }
            if (timerId === undefined) {
                timerId = setTimeout(timerExpired, wait);
            }
            return result;
        }
        debounced.cancel = cancel;
        debounced.flush = flush;
        return debounced;
    }


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


    // add a full-height gradient to post lists
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


    // add some html to post bodies that I can't do with markdown
    function beautifyPost(post) {
        // add title-note <span>s to parens in headings
        forEach(post.querySelectorAll('h1, h2, h3'), function (heading) {
            heading.innerHTML = heading.innerHTML.replace(/\(.*?\)/g, '<span class="title-note">$&</span>');
        });
        forEach(post.querySelectorAll('img[title]'), function (img) {
            var figure = document.createElement('figure'),
                figcaption = document.createElement('figcaption'),
                text = img.getAttribute('title');

            figcaption.innerHTML = text;

            img.parentNode.insertBefore(figure, img);
            figure.appendChild(img);
            figure.appendChild(figcaption);
        });
    }
    forEach(document.getElementsByClassName('article-body'), beautifyPost);


    // careful, now
    forEach(document.getElementsByClassName('admin-list__remove'), function (el) {
        el.addEventListener('click', function (ev) {
            if (!el.classList.contains('is-primed')) {
                ev.preventDefault();
                el.classList.add('is-primed');
            }
        });
    });


    // live markdown preview when editing
    function updateMarkdownPreviews(source, previews) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                forEach(previews, function (preview) {
                    preview.innerHTML = xhr.responseText;
                    beautifyPost(preview);
                    source.style.minHeight = preview.clientHeight + 'px';
                });
            }
        };
        xhr.open('POST', '/api/markdown/');
        xhr.send(source.value);
    }
    forEach(document.querySelectorAll('[data-markdown-preview]'), function (textarea) {
        var previews = document.querySelectorAll(textarea.getAttribute('data-markdown-preview'));
        if (!previews) {
            return false;
        }
        updateMarkdownPreviews(textarea, previews);
        textarea.addEventListener('keyup', debounce(function (ev) {
            updateMarkdownPreviews(textarea, previews);
        }, 400));
    });



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
