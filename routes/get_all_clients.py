from flask import jsonify

def get_all_clients_route(Client):
    def get_all_clients():
        try:
            clients = Client.query.with_entities(
                Client.id,
                Client.salutation,
                Client.first_name,
                Client.middle_name,
                Client.last_name,
                Client.existing,
                Client.CIF_number,
                Client.status
            ).all()
            clients_list = []
            for client in clients:
                name_parts = []
                if client.salutation:
                    name_parts.append(client.salutation.value)
                if client.first_name:
                    name_parts.append(client.first_name)
                if client.middle_name:
                    name_parts.append(client.middle_name)
                if client.last_name:
                    name_parts.append(client.last_name)
                full_name = " ".join(name_parts)
                clients_list.append({
                    "id": client.id,
                    "name": full_name,
                    "firstName": client.first_name or "",
                    "middleName": client.middle_name or "",
                    "lastName": client.last_name or "",
                    "salutation": client.salutation.value if client.salutation else "",
                    "existing": client.existing,
                    "CIF_number": client.CIF_number,
                    "status": client.status.value if client.status else ""
                })
            return jsonify({
                "clients": clients_list,
                "total_count": len(clients_list)
            }), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    return get_all_clients
