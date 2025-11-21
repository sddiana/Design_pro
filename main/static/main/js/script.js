function confirmDelete(categoryName, applicationsCount) {
    if (applicationsCount > 0) {
        return confirm(`Вы уверены, что хотите удалить категорию "${categoryName}"?\n\nБудут удалены все ${applicationsCount} заявок этой категории.\nЭто действие нельзя отменить.`);
    } else {
        return confirm(`Вы уверены, что хотите удалить категорию "${categoryName}"?`);
    }
}