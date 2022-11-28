from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np

from .models import Comment, Cluster

def update_clusters(is_new_user):
    num_reviews = Comment.objects.count()
    print(num_reviews)
    update_step = 6
    print(update_step)
    if num_reviews % update_step == 0 or is_new_user:
        all_user_names = list(map(lambda x: x.username, User.objects.only("username")))
        all_product_ids = set(map(lambda x: x.product.id, Comment.objects.only("product")))
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_product_ids) + 1), dtype=np.float32)
        for i in range(num_users):  # each user corresponds to a row, in the order of all_user_names
            user_reviews = Comment.objects.filter(user_name=all_user_names[i])
            for user_review in user_reviews:
                ratings_m[i, user_review.product.id] = user_review.rating
        
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())

        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}

        for cluster in new_clusters.values():
            cluster.save()
        for i, cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))

        print(new_clusters)