import tkinter as tk
import time

class HanoiVisualizer:
    def __init__(self, master, num_disks):
        self.master = master
        self.master.configure(bg="#ffe6f0")
        self.num_disks = num_disks
        self.canvas = tk.Canvas(master, width=600, height=320, bg="#fff0f5", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.towers = [[], [], []]  # Three towers
        for i in range(num_disks, 0, -1):
            self.towers[0].append(i)

        self.disk_ids = {}
        self.draw_title()
        self.draw_towers()
        self.draw_disks()

    def draw_title(self):
        self.canvas.create_text(
            300, 20,
            text="Hanoi Tower",
            fill="#cc3366",
            font=("Helvetica", 15, "bold"),
            tags="title"
        )

    def draw_towers(self):
        for i in range(3):
            x = 100 + i * 200
            # base
            self.canvas.create_rectangle(x - 60, 250, x + 60, 260, fill="#ffb6c1", outline="")
            # post
            self.canvas.create_rectangle(x - 5, 100, x + 5, 250, fill="#ff69b4", outline="")

    def draw_disks(self):
        self.canvas.delete("disk")
        pink_shades = ["#ffc0cb", "#ff99cc", "#ff66b2", "#ff3399", "#ff1a8c", "#e60073"]
        for i, tower in enumerate(self.towers):
            x_center = 100 + i * 200
            for j, size in enumerate(tower):
                width = size * 20
                y = 250 - j * 20
                color = pink_shades[(size - 1) % len(pink_shades)]
                disk = self.canvas.create_rectangle(
                    x_center - width // 2, y - 10,
                    x_center + width // 2, y + 10,
                    fill=color, outline="", tags="disk"
                )
                self.disk_ids[size] = disk
        self.master.update()
        time.sleep(0.4)

    def move_disk(self, source, target):
        if not self.towers[source]:
            print(f"Invalid move from tower {source + 1} to {target + 1}")
            return
        disk = self.towers[source].pop()
        if self.towers[target] and self.towers[target][-1] < disk:
            print(f"Invalid move: cannot place disk {disk} on smaller disk {self.towers[target][-1]}")
            self.towers[source].append(disk)
            return
        self.towers[target].append(disk)
        self.draw_disks()

def solve_hanoi(n, source, target, auxiliary, move_callback):
    if n == 1:
        move_callback(source, target)
        return
    solve_hanoi(n - 1, source, auxiliary, target, move_callback)
    move_callback(source, target)
    solve_hanoi(n - 1, auxiliary, target, source, move_callback)

def main():
    while True:
        try:
            num_disks = int(input("Enter number of disks (2 to 6): "))
            if 2 <= num_disks <= 6:
                break
            else:
                print("Please enter a number between 2 and 6.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            start_tower = int(input("Enter starting tower (1 to 3): ")) - 1
            end_tower = int(input("Enter target tower (1 to 3): ")) - 1
            if 0 <= start_tower <= 2 and 0 <= end_tower <= 2 and start_tower != end_tower:
                break
            else:
                print("Invalid towers. Start and end towers must be different and between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter integers.")

    auxiliary_tower = 3 - start_tower - end_tower

    root = tk.Tk()
    root.title("🎀 Hanoi Tower 🎀")
    root.configure(bg="#ffe6f0")

    visualizer = HanoiVisualizer(root, num_disks)

    root.after(1000, lambda: solve_hanoi(
        num_disks,
        start_tower,
        end_tower,
        auxiliary_tower,
        visualizer.move_disk
    ))

    root.mainloop()

if __name__ == "__main__":
    main()
