// browser test
if (!Modernizr.csstransforms) {
    var message = document.createElement('p');
    message.className = 'browser-message';
    message.innerHTML = 'Hey there. This site looks kind of a mess, huh? Unfortunately I\'m not going to be spending the time to support outdated browsers like this one, so please <a href="//outdatedbrowser.com/">upgrade</a>. I promise it\'ll make the web a better place.';
    document.body.insertBefore(message, document.body.firstChild);
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
    function isSymbol(value) {
      return typeof value == 'symbol' ||
            (isObjectLike(value) && objectToString.call(value) == symbolTag);
    }
    function isObjectLike(value) {
        return !!value && typeof value == 'object';
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
        var toggleList = [],
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
            toggleList = [];
            add(document.querySelectorAll('[data-toggle-target]'));
        }

        return {
            add: add,
            list: list,
            init: init
        };
    }());


    ////////////////
    //  Parallax  //
    ////////////////

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


    //////////////////////
    //  Beautification  //
    //////////////////////


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
    function colorizeAllPostLists() {
        forEach(document.getElementsByClassName('post-list'), colorizePostList);
    }
    colorizeAllPostLists();


    // add some html to post bodies that I can't do with markdown
    function beautifyPost(post) {
        // add title-note <span>s to parens in headings
        forEach(post.querySelectorAll('h1, h2, h3'), function (heading) {
            heading.innerHTML = heading.innerHTML.replace(/\(.*?\)/g, '<span class="title-note">$&</span>');
        });
        // wrap images with captions into <figure> elements
        forEach(post.querySelectorAll('img[title]'), function (img) {
            var figure = document.createElement('figure'),
                figcaption = document.createElement('figcaption'),
                text = img.getAttribute('title');

            figcaption.innerHTML = text;

            img.parentNode.insertBefore(figure, img);
            figure.appendChild(img);
            figure.appendChild(figcaption);

            // remove only-child figures from restrictive paragraphs
            var p = figure.parentNode;
            if (p.childNodes.length == 1) {
                p.parentNode.insertBefore(figure, p);
                p.parentNode.removeChild(p);
            }
        });
        // create table of contents based on fragments
        var toc = document.createElement('div'),
            fragments = post.querySelectorAll('.fragment'),
            links = [];
        if (fragments.length > 0) {
            forEach(post.querySelectorAll('.fragment'), function (fragment) {
                links.push('<a href="#' + fragment.id + '">' + fragment.innerHTML.toLowerCase() + '</a>');
            });
            toc.className = 'article-contents';
            toc.innerHTML = '<span class="article-contents__label">Contents:</span> ' +
                links.join(',&nbsp; ');
            post.insertBefore(toc, post.children[0]);
        }
    }
    forEach(document.getElementsByClassName('article-body'), beautifyPost);



    /////////////////////////////////
    //  Form element enhancements  //
    /////////////////////////////////


    // update label with input value
    function updateRangeLabel(label, input) {
        var result = '',
            suffix = input.getAttribute('data-value-suffix') || '',
            min = input.getAttribute('min') || 0,
            max = input.getAttribute('max') || 0,
            minDescription = input.getAttribute('data-min-description') || '',
            maxDescription = input.getAttribute('data-max-description') || '';
        if (input.value == min && minDescription) {
            result = minDescription;
        } else if (input.value == max && maxDescription) {
            result = maxDescription;
        } else {
            result = input.value + ' ' + suffix;
        }
        label.innerHTML = result;
    }
    function attachRangeLabel(label) {
        var input = document.getElementById(label.getAttribute('data-from-input'));
        updateRangeLabel(label, input);
        input.addEventListener('input', function () {
            updateRangeLabel(label, input);
        });
    }
    function attachAllRangeLabels() {
        forEach(document.querySelectorAll('[data-from-input]'), attachRangeLabel);
    }
    attachAllRangeLabels();

    // paired range inputs
    function constrainRangeInput(input, constrainer, constraint) {
        constrainer.addEventListener('input', function (ev) {
            var val = parseInt(input.value, 10),
                val2 = parseInt(constrainer.value, 10),
                ev = new UIEvent('input', { 'view': window, 'bubbles': true, 'cancelable': true });
            if (constraint === 'max' && val >= val2) {
                input.value = val2 - 1;
                input.dispatchEvent(ev);
            } else if (constraint === 'min' && val <= val2) {
                input.value = val2 + 1;
                input.dispatchEvent(ev);
            }
        });
    }
    function attachAllRangeConstraints() {
        forEach(document.querySelectorAll('[data-constrain-high]'), function (input) {
            var constrainer = document.getElementById(input.getAttribute('data-constrain-high'));
            constrainRangeInput(input, constrainer, 'max');
        });
        forEach(document.querySelectorAll('[data-constrain-low]'), function (input) {
            var constrainer = document.getElementById(input.getAttribute('data-constrain-low'));
            constrainRangeInput(input, constrainer, 'min');
        });
    }
    attachAllRangeConstraints();



    ////////////////////////////////
    //  Review list enhancements  //
    ////////////////////////////////


    // update a query string with new/changed/deleted param
    function updateQueryString(key, value, url) {
        if (!url) url = window.location.href;
        var re = new RegExp("([?&])" + key + "=.*?(&|#|$)(.*)", "gi"),
            hash;

        if (re.test(url)) {
            if (typeof value !== 'undefined' && value !== null) {
                return url.replace(re, '$1' + key + "=" + value + '$2$3');
            } else {
                hash = url.split('#');
                url = hash[0].replace(re, '$1$3').replace(/(&|\?)$/, '');
                if (typeof hash[1] !== 'undefined' && hash[1] !== null)
                    url += '#' + hash[1];
                return url;
            }
        }
        else {
            if (typeof value !== 'undefined' && value !== null) {
                var separator = url.indexOf('?') !== -1 ? '&' : '?';
                hash = url.split('#');
                url = hash[0] + separator + key + '=' + value;
                if (typeof hash[1] !== 'undefined' && hash[1] !== null) {
                    url += '#' + hash[1];
                }
                return url;
            } else {
                return url;
            }
        }
    }

    // update post list with ajax
    function updateSearchArea(container, url) {
        var xhr = new XMLHttpRequest(),
            containerId = container.id,
            tmp = document.createElement('div'),
            fragment;

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                tmp.innerHTML = xhr.responseText;
                fragment = tmp.querySelector('#' + containerId);
                container.innerHTML = fragment.innerHTML;
                window.history.pushState('', '', url);

                searchArea = document.getElementById('search-area');

                attachAllRangeLabels();
                attachAllRangeConstraints();
                attachAllRangeChanges();
                colorizeAllPostLists();
                toggles.init();
            }
        };
        xhr.open('GET', url);
        xhr.send(null);
    }

    function attachAllRangeChanges() {
        forEach(document.querySelectorAll('.search-refine input[type="range"]'), function (input) {
            input.addEventListener('change', debounce(function () {
                updateSearchArea(searchArea, updateQueryString(input.name, input.value));
            }), 400);
        });
    }

    var searchArea = document.getElementById('search-area');
    if (searchArea) {
        attachAllRangeChanges();
        document.body.addEventListener('click', function (ev) {
            if (ev.target.tagName.toLowerCase() === 'a' &&
                (getParentsByClassName(ev.target, 'search-refine').length > 0 ||
                getParentsByClassName(ev.target, 'search-current-filters').length > 0)) {
                ev.preventDefault();
                updateSearchArea(searchArea, ev.target.href);
            }
        });
    }



    //////////////////////////////
    //  Admin area enhancements //
    //////////////////////////////


    // careful, now
    forEach(document.getElementsByClassName('careful-remove'), function (el) {
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


    // make copying a file url more convenient
    forEach(document.getElementsByClassName('admin-image-list'), function (list) {
        // delegate clicks to grid
        list.addEventListener('click', function (ev) {
            if (ev.target.tagName.toLowerCase() === 'img') {
                var item = getParentsByClassName(ev.target, 'admin-image-list__item')[0],
                    input;
                if (!item) {
                    return false;
                }
                input = item.querySelector('.admin-image-list__filename');
                if (item.classList.contains('is-active')) {
                    item.classList.remove('is-active');
                    input.blur();
                } else {
                    item.classList.add('is-active');
                    input.focus();
                }
            }
        });
    });


    // get image dimensions for an image grid item
    // expects an .image-grid__item node
    function updateImageDimensions(img, target) {
        if (img && target) {
            // reasonable wait for image data load
            window.setTimeout(function () {
                target.innerHTML = img.naturalWidth + 'x' + img.naturalHeight;
            }, 1000);
        }
    }
    forEach(document.getElementsByClassName('admin-image-list__item'), function (item) {
        updateImageDimensions(item.querySelector('.image-grid__image'), item.querySelector('.image-grid__size'));
    });


    // convenient upload selectors for post writing
    // end result is writing a file path to a particular input
    // written after alcohol, revisit later
    var imageSelectorTriggers = document.querySelectorAll('[data-fills-image-input]'),
        imageSelector = document.createElement('div'),
        imageSelectorGrid = document.createElement('div'),
        imageSelectorPath = '',
        imageSelectorCurrentInput;
    imageSelector.className = 'image-selector';
    imageSelectorGrid.className = 'image-selector__items image-grid grid grid--compact';
    imageSelector.appendChild(imageSelectorGrid);
    document.body.appendChild(imageSelector);

    function loadImages(order, callback) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                callback(JSON.parse(xhr.responseText));
            }
        };
        xhr.open('GET', '/api/files/?order=' + order)
        xhr.send(null);
    }

    function makeImageSelectorItem(data) {
        var result = document.createElement('div'),
            img = document.createElement('img'),
            filename = document.createElement('span'),
            size = document.createElement('span'),
            date = document.createElement('span');

        result.className = 'image-selector__item image-grid__item grid__unit';
        img.className = 'image-selector__image image-grid__image';
        img.src = imageSelectorPath + data[0];
        filename.className = 'image-selector__filename image-grid__filename';
        filename.innerHTML = data[0];
        size.className = 'image-selector__size image-grid__size';
        updateImageDimensions(img, size);
        date.className = 'image-selector__date image-grid__date';
        date.innerHTML = data[2];

        result.appendChild(img);
        result.appendChild(filename);
        result.appendChild(size);
        result.appendChild(date);
        return result;
    }

    function refreshImageSelector(order) {
        imageSelectorGrid.innerHTML = '<div class="grid__unit">Loading ...</div>';
        loadImages(order, function (response) {
            var result = document.createDocumentFragment();
            imageSelectorPath = response.path;
            forEach(response.files, function (file) {
                result.appendChild(makeImageSelectorItem(file));
            });
            imageSelectorGrid.innerHTML = '';
            imageSelectorGrid.appendChild(result);
        });
    }

    if (imageSelectorTriggers) {
        forEach(imageSelectorTriggers, function (trigger) {
            trigger.addEventListener('click', function (ev) {
                if (!imageSelector.classList.contains('is-active')) {
                    refreshImageSelector('time');
                    imageSelector.classList.add('is-active');
                    imageSelectorCurrentInput = document.getElementById(trigger.getAttribute('data-fills-image-input'));
                }
            });
        });
        imageSelector.addEventListener('click', function (ev) {
            var items = getParentsByClassName(ev.target, 'image-selector__item');
            if (items.length > 0) {
                imageSelectorCurrentInput.value = imageSelectorPath + items[0].getElementsByClassName('image-selector__filename')[0].innerHTML;
            }
            imageSelector.classList.remove('is-active');
        });
    }


    // list the files selected in a multiple file upload
    function listFiles(input, list) {
        var listItem = document.createElement('li');
        listItem.className = 'item-list__item';
        list.innerHTML = '';
        forEach(input.files, function (file) {
            var clone = listItem.cloneNode(true);
            clone.innerHTML = file.name;
            list.appendChild(clone);
        });
    }
    forEach(document.querySelectorAll('input[type="file"][data-lists-to]'), function (input) {
        var list = document.getElementById(input.getAttribute('data-lists-to'));
        listFiles(input, list);
        input.addEventListener('change', function (ev) {
            listFiles(input, list);
        });
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
