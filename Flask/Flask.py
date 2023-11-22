from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        film_name = data.get('film_name', "")

        film_genre_query = {
            "query": {
                "match": {
                    "title": film_name
                }
            },
            "_source": ["genre_ids"]
        }

        film_genre_result = es.search(index='movie', body=film_genre_query)

        if film_genre_result['hits']['hits']:
            genre_ids = film_genre_result['hits']['hits'][0]['_source']['genre_ids']

            recommendations = []

            for genre_id in genre_ids:
                similar_genre_query = {
                    "query": {
                        "term": {
                            "genre_ids": genre_id
                        }
                    }
                }

                similar_genre_result = es.search(index='movie', body=similar_genre_query)

                app.logger.info(f"Similar Genre Result for genre_id {genre_id}: {similar_genre_result}")

                recommendations.extend([hit['_source'] for hit in similar_genre_result['hits']['hits']])

            if not recommendations:
                return jsonify({'info': f'No Recommendations for the film "{film_name}".'})
            else:
                # Include additional fields in the response
                formatted_recommendations = [
                    {
                        'title': movie['title'],
                        'original_language': movie['original_language'],
                        'overview': movie['overview'],
                        'backdrop_path': 'https://image.tmdb.org/t/p/original/' + movie['backdrop_path']
                    }
                    for movie in recommendations
                ]

                return jsonify({'recommendations': formatted_recommendations})
        else:
            return jsonify({'info': 'Film Not Offered Yet'})

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    try:
        data = request.get_json()
        prefix = data.get('prefix', "")

        # Elasticsearch prefix query for autocomplete
        autocomplete_query = {
            "query": {
                "prefix": {
                    "title.keyword": prefix.lower()
                }
            },
            "_source": ["title"],
            "size": all  
        }

        autocomplete_result = es.search(index='movie', body=autocomplete_query)

        suggestions = [hit['_source']['title'] for hit in autocomplete_result['hits']['hits']]
        
        return jsonify({'suggestions': suggestions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
