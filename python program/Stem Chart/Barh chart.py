import matplotlib.pyplot as plt

books = ["Mahabharat","Time Is Money","Avengers : Doomsday","The Hunter Game","Faith","The Graveyard Book","His & Hers","The HomeComing"]

sales = [12250,21020,11500,11150,1350,13690,11101,11000]

plt.figure(figsize=(12,6))
plt.barh(books,sales)
plt.yticks(fontsize=8)
plt.show()