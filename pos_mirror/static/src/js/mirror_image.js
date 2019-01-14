$(document).ready(function() {
    setInterval(function() {
        $.getJSON("/pos/mirror_data", function(result) {
            var product_data = "";
            var symbol = result['currency'];
            if (result['name'] != '[]') {
                var obj = eval(result['name']);
                if (obj.length != 0){
                    for (var i = 0; i < obj.length - 1; i++) {
                        product_data +=
                            "<tr><td class='product_name'><b>" +
                            obj[i][0] +
                            "</b><br/><span class='product_price'>" +
                            obj[i][2] + " " + obj[i][3] +
                            " at " + obj[i][1].toFixed(2) +
                            "" + symbol + "/" + obj[i][3] +
                            "</span>";
                        if (obj[i][4] != 0) {
                            product_data +=
                                "<br/><span class='product_price'>With a " +
                                obj[i][4] +
                                "% discount</span></td>";
                        }
                        product_data +=
                            "<td class='product_name1'><b>" +
                            ((obj[i][1] * obj[i][2]) - (obj[
                                i][2] * (obj[i][1] *
                                obj[i][4] * .01))).toFixed(
                                2) + "" + symbol +
                            "</b></td></tr>";
                    }
                    $(".total_amount").html("Total:" 
                        + obj[obj.length - 1][0].toFixed(2) 
                        + " " + symbol);
                    console.log("textes", obj[obj.length - 1][0]);
                    $(".total_tax").html("Taxes:" 
                        + obj[obj.length - 1][1].toFixed(2)
                        + " " + symbol);
                }
                if (obj.length <= 1) {
                    $(".total_amount").html("");
                    $(".total_tax").html("");
                    product_data =
                        "<div class='empty'>Your shopping cart is empty</div>"
                }
                $(".product_content").html(product_data);
            } else {
                $(".total_amount").html("");
                $(".total_tax").html("");
                $(".product_content").html(
                    "<div class='empty'>Your shopping cart is empty</div>"
                );
            }
            $('.product_list').scrollTop(
                99999999999999999);
        }).fail(function() {
            if (window.location.pathname ==
                '/pos/mirror')
                window.location.reload();
        });
    }, 2000);
});
