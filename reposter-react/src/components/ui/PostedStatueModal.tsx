import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function PostedStatusModal(props: any) {
    return (
        <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Modal heading
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h4>Centered Modal</h4>
                <p>
                    {props.status}
                    {props.services && props.services.map((service: any) => {
                        return (
                            <div key={service.id}>
                                {service.service}
                                {service.status}
                            </div>
                        );
                    })}
                </p>
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.onHide}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
}

export default PostedStatusModal;