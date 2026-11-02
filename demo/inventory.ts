/** Supplies carried by a wastelander. */
export interface Item {
  name: string;
  weight: number;
  tags?: string[];
}

const MAX_WEIGHT = 200;

export class Inventory {
  private readonly items = new Map<string, Item>();

  constructor(private readonly owner: string) {}

  add(item: Item): boolean {
    const total = this.weight() + item.weight;
    if (total > MAX_WEIGHT) {
      console.warn(`Overencumbered: ${this.owner} (${total}/${MAX_WEIGHT})`);
      return false;
    }
    this.items.set(item.name, item);
    return true;
  }

  weight(): number {
    return [...this.items.values()].reduce((sum, i) => sum + i.weight, 0);
  }

  find(pattern: RegExp): Item[] {
    return [...this.items.values()].filter((i) => pattern.test(i.name));
  }
}

const pack = new Inventory("Courier");
pack.add({ name: "Stimpak", weight: 0.5, tags: ["medicine"] });
pack.add({ name: "Water", weight: 1 });
console.log(pack.find(/^st/i), pack.weight());
