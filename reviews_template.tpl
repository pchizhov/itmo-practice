<!-- news_template.tpl -->
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Review</th>
                <th>Food</th>
                <th>Service</th>
                <th>Ambiance</th>
                <th>Price</th>
                <th>Location</th>
                <th></th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td>{{ row.text }}</td>
                    <td class="food"><a href="/add_cat/?cat=food&id={{ row.id }}">{{ row.food }}</a></td>
                    <td class="service"><a href="/add_cat/?cat=service&id={{ row.id }}">{{ row.service }}</a></td>
                    <td class="ambiance"><a href="/add_cat/?cat=ambiance&id={{ row.id }}">{{ row.ambiance }}</a></td>
                    <td class="price"><a href="/add_cat/?cat=price&id={{ row.id }}">{{ row.price }}</a></td>
                    <td class="location"><a href="/add_cat/?cat=location&id={{ row.id }}">{{ row.location }}</a></td>
                    <td class="mark"><a href="/update/?id={{ row.id }}" class="ui right floated small primary button">submit</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/new_restaurant" class="ui right floated small primary button">Wanna more reviews!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>