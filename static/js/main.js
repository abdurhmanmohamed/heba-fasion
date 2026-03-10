
(function ($) {
    "use strict";

    /*[ Load page ]
    ===========================================================*/
    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<div class="loader05"></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: [ 'animation-duration', '-webkit-animation-duration'],
        overlay : false,
        overlayClass : 'animsition-overlay-slide',
        overlayParentElement : 'html',
        transition: function(url){ window.location.href = url; }
    });
    
    /*[ Back to top ]
    ===========================================================*/
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display','flex');
        } else {
            $("#myBtn").css('display','none');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });


    /*==================================================================
    [ Fixed Header ]*/
    var headerDesktop = $('.container-menu-desktop');
    var wrapMenu = $('.wrap-menu-desktop');

    if($('.top-bar').length > 0) {
        var posWrapHeader = $('.top-bar').height();
    }
    else {
        var posWrapHeader = 0;
    }
    

    if($(window).scrollTop() > posWrapHeader) {
        $(headerDesktop).addClass('fix-menu-desktop');
        $(wrapMenu).css('top',0); 
    }  
    else {
        $(headerDesktop).removeClass('fix-menu-desktop');
        $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
    }

    $(window).on('scroll',function(){
        if($(this).scrollTop() > posWrapHeader) {
            $(headerDesktop).addClass('fix-menu-desktop');
            $(wrapMenu).css('top',0); 
        }  
        else {
            $(headerDesktop).removeClass('fix-menu-desktop');
            $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
        } 
    });


    /*==================================================================
    [ Menu mobile ]*/
    $('.btn-show-menu-mobile').on('click', function(){
        $(this).toggleClass('is-active');
        $('.menu-mobile').slideToggle();
    });

    var arrowMainMenu = $('.arrow-main-menu-m');

    for(var i=0; i<arrowMainMenu.length; i++){
        $(arrowMainMenu[i]).on('click', function(){
            $(this).parent().find('.sub-menu-m').slideToggle();
            $(this).toggleClass('turn-arrow-main-menu-m');
        })
    }

    $(window).resize(function(){
        if($(window).width() >= 992){
            if($('.menu-mobile').css('display') == 'block') {
                $('.menu-mobile').css('display','none');
                $('.btn-show-menu-mobile').toggleClass('is-active');
            }

            $('.sub-menu-m').each(function(){
                if($(this).css('display') == 'block') { console.log('hello');
                    $(this).css('display','none');
                    $(arrowMainMenu).removeClass('turn-arrow-main-menu-m');
                }
            });
                
        }
    });


    /*==================================================================
    [ Show / hide modal search ]*/
    $('.js-show-modal-search').on('click', function(){
        $('.modal-search-header').addClass('show-modal-search');
        $(this).css('opacity','0');
    });

    $('.js-hide-modal-search').on('click', function(){
        $('.modal-search-header').removeClass('show-modal-search');
        $('.js-show-modal-search').css('opacity','1');
    });

    $('.container-search-header').on('click', function(e){
        e.stopPropagation();
    });


    /*==================================================================
    [ Isotope ]*/
    var $topeContainer = $('.isotope-grid');
    var $filter = $('.filter-tope-group');

    // filter items on button click
    $filter.each(function () {
        $filter.on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $topeContainer.isotope({filter: filterValue});
        });
        
    });

    // init Isotope
    $(window).on('load', function () {
        var $grid = $topeContainer.each(function () {
            $(this).isotope({
                itemSelector: '.isotope-item',
                layoutMode: 'fitRows',
                percentPosition: true,
                animationEngine : 'best-available',
                masonry: {
                    columnWidth: '.isotope-item'
                }
            });
        });
    });

    var isotopeButton = $('.filter-tope-group button');

    $(isotopeButton).each(function(){
        $(this).on('click', function(){
            for(var i=0; i<isotopeButton.length; i++) {
                $(isotopeButton[i]).removeClass('how-active1');
            }

            $(this).addClass('how-active1');
        });
    });

    /*==================================================================
    [ Filter / Search product ]*/
    $('.js-show-filter').on('click',function(){
        $(this).toggleClass('show-filter');
        $('.panel-filter').slideToggle(400);

        if($('.js-show-search').hasClass('show-search')) {
            $('.js-show-search').removeClass('show-search');
            $('.panel-search').slideUp(400);
        }    
    });

    $('.js-show-search').on('click',function(){
        $(this).toggleClass('show-search');
        $('.panel-search').slideToggle(400);

        if($('.js-show-filter').hasClass('show-filter')) {
            $('.js-show-filter').removeClass('show-filter');
            $('.panel-filter').slideUp(400);
        }    
    });




    /*==================================================================
    [ Cart ]*/
    $('.js-show-cart').on('click',function(){
        $.ajax({
        url: "/get-cart-items",
        method: "POST",
        success: function(response){
                // update text
                document.getElementById("total-price").innerText = response.total_price + " E£";
                $('#cart-items').html('');
                response.items.forEach(function(item){
                let cartElement = `
                <li class="cart-item d-flex align-items-center p-2 mb-2 rounded">
                    <!-- Product image -->
                    <div class="cart-item-img">
                        <img src="${item.img}" alt="IMG" />
                    </div>

                    <!-- Name + Price -->
                    <div class="cart-item-info flex-grow-1 ms-2">
                        <div class="cart-item-name">${item.name}</div>
                        <div class="cart-item-price">${item.amount} x ${item.price} E£</div>
                    </div>

                    <!-- Trash button -->
                    <button class="cart-delete-btn ms-2" data-id="${item.id}">
                        <i class="fa fa-trash"></i>
                    </button>
                </li>
                `;
                    $('#cart-items').append(cartElement);
                    $(document).on('click', '.cart-delete-btn', function(){
                    let item_id = $(this).data('id');

                    // Example: remove item from DOM
                    $(this).closest('li').remove();

                    // Optional: send request to server
                    
                    $.ajax({
                        url: "/remove-cart-item",
                        method: "POST",
                        data: {id: item_id},
                        success: function(response){
                            $('#total-price').html('');
                            $('#total-price').text(response.total_price + " E£");
                            console.log("Item removed from server");
                        }
                    });
                });
                });

                // update colors
                // $('#color').html('');
                // response.colors.forEach(function(color){
                //     $('#color').append(`<option>${color}</option>`);
                // });


                // show modal
            }

        })
        $('.js-panel-cart').addClass('show-header-cart');
    });

    $('.js-hide-cart').on('click',function(){
        $('.js-panel-cart').removeClass('show-header-cart');
    });

    /*==================================================================
    [ Cart ]*/
    $('.js-show-sidebar').on('click',function(){
        $('.js-sidebar').addClass('show-sidebar');
    });

    $('.js-hide-sidebar').on('click',function(){
        $('.js-sidebar').removeClass('show-sidebar');
    });

    /*==================================================================
    [ +/- num product ]*/

 /*==================================================================
[ +/- num product ]*/
$('.btn-num-product-down').on('click', function(){
    let item_id = $(this).data('id');
    let $input = $(`.num-product[data-id='${item_id}']`);
    let $totalCell = $(`.total_item_price[data-id='${item_id}']`);

    var numProduct = Number($input.val());
    if(numProduct > 0) numProduct -= 1;
    $input.val(numProduct);

    $.ajax({
        url: "/change-amount",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({id: item_id, amount: numProduct}),
        success: function(response){
            if(response.removed){
                $(`tr[data-id='${item_id}']`).remove();
            } else {
                $totalCell.text(response.price * numProduct + " E£");
            }
            $('.total_price').text(response.total_price + " E£");  // if you have a cart total element
        }
    });
});

$('.btn-num-product-up').on('click', function(){
    let item_id = $(this).data('id');
    let $input = $(`.num-product[data-id='${item_id}']`);
    let $totalCell = $(`.total_item_price[data-id='${item_id}']`);

    var numProduct = Number($input.val());
    numProduct += 1;
    $input.val(numProduct);

    $.ajax({
        url: "/change-amount",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({id: item_id, amount: numProduct}),
        success: function(response){
            $totalCell.text(response.price * numProduct + " E£");
            $('.total_price').text(response.total_price + " E£");  // update cart total
        }
    });
});

    /*==================================================================
    [ Rating ]*/
    $('.wrap-rating').each(function(){
        var item = $(this).find('.item-rating');
        var rated = -1;
        var input = $(this).find('input');
        $(input).val(0);

        $(item).on('mouseenter', function(){
            var index = item.index(this);
            var i = 0;
            for(i=0; i<=index; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });

        $(item).on('click', function(){
            var index = item.index(this);
            rated = index;
            $(input).val(index+1);
        });

        $(this).on('mouseleave', function(){
            var i = 0;
            for(i=0; i<=rated; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });
    });
    
    /*==================================================================
    [ Show modal1 ]*/
    $(document).on('click', '.js-show-modal1', function(e){
        e.preventDefault();

        let item_id = $(this).data('id');

        $.ajax({
            url: "/get-item",
            method: "POST",
            data: {id: item_id},

            success: function(response){
                // update text

                if ($('.slick3').hasClass('slick-initialized')) {
                    $('.slick3').slick('unslick');
                }
                $('#name').text(response.name);
                $('#price').text(response.price + " E£");
                $('#description').text(response.description);

                // update images
                $('#all_item_imgs').html('');
                response.images.forEach(function(img){
                    let imageElement = `
                        <div class="item-slick3" data-thumb="${img}">
                            <div class="wrap-pic-w pos-relative">
                                <img src="${img}" alt="IMG-PRODUCT" height="420">
                                <a class="flex-c-m size-108 how-pos1 bor0 fs-16 cl10 bg0 hov-btn3 trans-04" href="${img}">
                                    <i class="fa fa-expand"></i>
                                </a>
                            </div>
                        </div>
                    `;
                    $('#all_item_imgs').append(imageElement);
                });

                // refresh slider **once**
                $('.wrap-slick3').each(function(){
                    $(this).find('.slick3').slick({
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        fade: true,
                        infinite: true,
                        autoplay: false,
                        autoplaySpeed: 6000,

                        arrows: true,
                        appendArrows: $(this).find('.wrap-slick3-arrows'),
                        prevArrow:'<button class="arrow-slick3 prev-slick3"><i class="fa fa-angle-left" aria-hidden="true"></i></button>',
                        nextArrow:'<button class="arrow-slick3 next-slick3"><i class="fa fa-angle-right" aria-hidden="true"></i></button>',

                        dots: true,
                        appendDots: $(this).find('.wrap-slick3-dots'),
                        dotsClass:'slick3-dots',
                        customPaging: function(slick,index){
                            var portrait = $(slick.$slides[index]).data('thumb');
                            return '<img src="'+portrait+'"/><div class="slick3-dot-overlay"></div>';
                        }
                    });
                });

                // update colors
                $('#color').html('');
                response.colors.forEach(function(color){
                    $('#color').append(`<option>${color}</option>`);
                });
                document.getElementById('popup').dataset.id = item_id;


                // show modal
                $('.js-modal1').addClass('show-modal1');
            }
        });
    });

    $('.js-hide-modal1').on('click', function(){
        $('.js-modal1').removeClass('show-modal1');
    });


    $('.js-hide-modal1').on('click', function(){

        $('.js-modal1').removeClass('show-modal1');
    });



})(jQuery);