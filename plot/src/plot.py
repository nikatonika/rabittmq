import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import os
import time


def error_distribution(log, image):
    while True:
        try:
            # Проверка наличия лог файла
            if os.path.exists(log):
                # Читаем данные из лог файла
                df = pd.read_csv(log)

                # проверка на наличие данных в файле csv
                if 'absolute_error' in df.columns and not df.empty:
                    #Построение гистограммы
                    plt.figure(figsize=(8, 6))
                    seaborn.histplot(
                        df["absolute_error"], 
                        kde=True, 
                        bins=10, 
                        color="orange", 
                        edgecolor="black", 
                        label="Гистограмма"
                    )

                    # линия распределения
                    seaborn.kdeplot(
                        data= df, 
                        x = "absolute_error", 
                        color="red", 
                        linewidth=2, 
                        label="Линия распределения"
                    )
                    plt.title("Распределение абсолютных ошибок", fontsize=14)
                    plt.xlabel("Абсолютная ошибка", fontsize=10)
                    plt.ylabel("Частота", fontsize=10)
                    plt.grid(True)

                    # Сохранение графика в файл
                    plt.savefig(image)
                    plt.close()
                    print(f"[OK] =========> Гистограмма обновлена: {image}")

            else:
                print(f"{log} Еще не создан.")

        except Exception as e:
            print(f"[FATAL] =========> Ошибка обновления гистограммы {e}")

        # Интервал обновления в секундах
        time.sleep(10)


log_file = "./logs/metric_log.csv"
output_image = "./logs/error_distribution.png"
error_distribution(log_file, output_image)
